from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Robot
from .forms import RobotForm

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from robots.models import Robot
from map.models import Map

@login_required
def set_current_robot(request, robot_id, page):
    user_robots = Robot.objects.filter(user=request.user)

    # Unset current flag for all maps
    user_robots.update(is_current=False)
    
    # Get the robot object or return 404 if not found
    robot = get_object_or_404(Robot, id=robot_id, user=request.user)
    
    # Set this robot as the current robot
    robot.is_current = True
    robot.save()
    
    # Redirect back to the robot list page or any other desired page
    return redirect(page)

@login_required
def user_robots(request):

    # Get the robots belonging to the logged-in user
    robots = Robot.objects.filter(user=request.user)
    current_robot = get_object_or_404(Robot, user=request.user, is_current=True)
    if not current_robot:
        current_robot = get_object_or_404(Robot, user=request.user).first() 
        current_robot.is_current = True         
        
    return render(request, 'robots/user_robots.html', {'robots': robots})

@login_required
def create_robot(request):
    if request.method == 'POST':
        form = RobotForm(request.POST)
        if form.is_valid():
            robot = form.save(commit=False)
            robot.user = request.user
            robot.is_current = False  # Ensure it is always False by default
            robot.save()
            return redirect('user_robots')
    else:
        form = RobotForm()
    return render(request, 'robots/create_robot.html', {'form': form})


@login_required
def edit_robot(request, robot_id):
    robot = get_object_or_404(Robot, id=robot_id, user=request.user)

    if request.method == 'POST':
        form = RobotForm(request.POST, instance=robot)
        if form.is_valid():
            robot = form.save(commit=False)
            robot.is_current = False  # Keep it False during editing
            robot.save()
            return redirect('user_robots')
    else:
        form = RobotForm(instance=robot)

    return render(request, 'robots/edit_robot.html', {'form': form, 'robot': robot})

@login_required
def delete_robot(request, robot_id):
    # Fetch the robot and ensure it belongs to the logged-in user
    robot = get_object_or_404(Robot, id=robot_id, user=request.user)
    # Delete the robot
    robot.delete()
    # Redirect to the user's robots page
    return redirect('user_robots')

def control_robot(request, robot_id):
    robot = Robot.objects.get(id=robot_id, user=request.user)  # Ensure the robot belongs to the user
    return redirect(f'/submit/?robot_ip={robot.nao_ip}&network_interface={robot.network_interface}&language={robot.language}&priority_driver=naoqi_driver')