import carla
import random
import pygame
import cv2
import numpy as np
import time
from datetime import datetime
import math


client = carla.Client('localhost',2000)
world = client.load_world('Town04')
# town weather
weather = carla.WeatherParameters(
    cloudiness=0.0,
    precipitation=0.0,
    sun_altitude_angle=10.0,
    sun_azimuth_angle = 70.0,
    precipitation_deposits = 0.0,
    wind_intensity = 0.0,
    fog_density = 0.0,
    wetness = 0.0, 
)
world.set_weather(weather)

bp_lib = world.get_blueprint_library() 
spawn_points = world.get_map().get_spawn_points()

vehicle_bp = bp_lib.find('vehicle.audi.etron')
ego_vehicle = world.try_spawn_actor(vehicle_bp, spawn_points[79])

spectator = world.get_spectator()
transform = carla.Transform(ego_vehicle.get_transform().transform(carla.Location(x=-1,z=3)),ego_vehicle.get_transform().rotation)
spectator.set_transform(transform)

# spawning autopilot vehicles
# for i in range(200):  
#     vehicle_bp = random.choice(bp_lib.filter('vehicle')) 
#     npc = world.try_spawn_actor(vehicle_bp, random.choice(spawn_points))

for v in world.get_actors().filter('*vehicle*'): 
    v.set_autopilot(True) 
ego_vehicle.set_autopilot(False) 

pygame.init() 

pygame.display.set_caption("CARLA Manual Control")
screen = pygame.display.set_mode((1920, 100))

control = carla.VehicleControl()
clock = pygame.time.Clock()
done = False

# Add collision sensor
# this is not working right now
#  collision_sensor_bp = bp_lib.find('sensor.other.collision')
# collision_sensor = world.spawn_actor(collision_sensor_bp, carla.Transform(), attach_to=ego_vehicle)
# def collision_event(event, time):
#     time = event.timestamp
#     print(time)
#     print("COLLIDE!")
# collision_time = None
# collision_sensor.listen(lambda e: collision_event(e, collision_time))

# Add RGB camera
camera_bp = bp_lib.find('sensor.camera.rgb') 
camera_init_trans = carla.Transform(carla.Location(x=0.4,y=-0.4, z=1.3), carla.Rotation(pitch=-15.0)) 
camera_bp.set_attribute("image_size_x", '1920')
camera_bp.set_attribute("image_size_y", '900')
camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=ego_vehicle)
image_w = camera_bp.get_attribute("image_size_x").as_int()
image_h = camera_bp.get_attribute("image_size_y").as_int()

def rgb_callback(image, data_dict):
    img = np.reshape(np.copy(image.raw_data), (image.height, image.width, 4)) #Reshaping with alpha channel
    img[:,:,3] = 255 #Setting the alpha to 255 
    data_dict['rgb_image'] = img
    # print("image captured")
sensor_data = {'rgb_image': np.zeros((image_h, image_w, 4))}
camera.listen(lambda image: rgb_callback(image, sensor_data))

reverse_limiter = 0
right_blinker_limiter = 0
left_blinker_limiter = 0

# popped up pedestrian
walker_controller_bp = bp_lib.find('controller.ai.walker')
walker_bp = random.choice(bp_lib.filter('*walker*'))
walker = world.try_spawn_actor(walker_bp, spawn_points[80])
last_shown_pedestrain_time = datetime.now()
def pedestrian(target, reaction_time, controller_bp, walker, world):
    vehicle_position = target.get_location()
    vehicle_speed = target.get_velocity()
    random_velocity = random.randint(-2,2)*vehicle_speed/(3*cal_speed(target))
    # print("vehicle position: ", vehicle_position, "| speed: ", vehicle_speed)
    walker_x_transformation = (vehicle_position + (vehicle_speed+random_velocity) * reaction_time).dot(carla.Vector3D(x=1))
    walker_y_transformation = (vehicle_position + (vehicle_speed+random_velocity) * reaction_time).dot(carla.Vector3D(y=1))
    walker_location = carla.Location(x=walker_x_transformation, y=walker_y_transformation, z=1)
    walker.set_location(walker_location)
    # print("pop a walker at: Location(x=", walker_x_transformation, ", y=:", walker_y_transformation," z=2)")
    # print("set prev walker at: ", walker_location.x)
    return walker_location

# determine if walker is collided
def walker_hit(walker, walker_deter, walker_prev_location):
    # print("walker now at: ", walker.get_location())
    # print("prev walker at: ", walker_prev_location)
    if (round(walker.get_location().x) != round(walker_prev_location.x) or round(walker.get_location().y) != round(walker_prev_location.y)):
        # print("CdddddwdwOLLIDED")
        return False, walker.get_location()
    else: return True, walker_prev_location


# calculating speed
def cal_speed(vehicle):
    vehicle_velocity = vehicle.get_velocity()
    x_direction = carla.Vector3D(x=1)
    y_direction = carla.Vector3D(y=1)
    z_direction = carla.Vector3D(z=1)
    speed_x = vehicle_velocity.dot(x_direction)
    speed_y = vehicle_velocity.dot(y_direction)
    speed_z = vehicle_velocity.dot(z_direction)
    speed = math.sqrt(speed_x**2 + speed_y**2 + speed_z**2)
    return speed

# see if user react in 0.8 secs
def user_reaction():
    reaction_time = 0.8

# calculating time difference
def time_diff(x, y):
    return x.second+60*x.minute+3600*x.hour - (y.second+60*y.minute+3600*y.hour)

# set initial velocity to zero
control.throttle = 0
control.brake = 10
ego_vehicle.apply_control(control)

# set walker being collided to false
walker_deter = False
walker_prev_location = carla.Location()
start_time = datetime.now()
end_time = datetime.now()
press_p_deter = False

#start ticking
while not done:

    keys = pygame.key.get_pressed() 

    # limit speed
    if (keys[pygame.K_UP] or keys[pygame.K_w]):
        if (cal_speed(ego_vehicle) > 20): control.throttle = 0.5
        else: control.throttle = min(control.throttle + 0.05, 1.0)
    else:
        control.throttle = 0.0

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        # print(control.brake)
        control.brake = min(control.brake + 50, 100.0)
        # print(control.brake)
    else:
        control.brake = 0.0

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        control.steer = max(control.steer - 0.05, -0.3)
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        control.steer = min(control.steer + 0.05, 0.3)
    else:
        control.steer = 0.0

    # reverse 
    if keys[pygame.K_q]:
        # print(control.reverse, " ", reverse_limiter)
        reverse_limiter += 1
        if reverse_limiter == 2:
            reverse_limiter = 0
            control.reverse = not control.reverse

    # blinker
    current_lights = carla.VehicleLightState.NONE
    if keys[pygame.K_z]:
        right_blinker_limiter += 1
        if right_blinker_limiter == 2:
            current_lights ^= carla.VehicleLightState.RightBlinker
            ego_vehicle.set_light_state(carla.VehicleLightState(current_lights))
            # print("right blinker on")
        elif right_blinker_limiter == 4:
            ego_vehicle.set_light_state(carla.VehicleLightState.NONE)
            right_blinker_limiter = 0
            # print("right blinker off")

    elif keys[pygame.K_x]:
        left_blinker_limiter += 1
        if left_blinker_limiter == 2:
            current_lights ^= carla.VehicleLightState.LeftBlinker
            ego_vehicle.set_light_state(carla.VehicleLightState(current_lights))
            print("left blinker on")
        elif left_blinker_limiter == 4:
            ego_vehicle.set_light_state(carla.VehicleLightState.NONE)
            left_blinker_limiter = 0
            print("left blinker off")
    
    control.hand_brake = keys[pygame.K_SPACE]
    
    if keys[pygame.K_p]:
        # walker_deter = False
        start_time = datetime.now()
        if (time_diff(start_time, last_shown_pedestrain_time) > 1):
            print("pedestrain shown at: {}:{}:{}".format(datetime.now().hour,datetime.now().minute,datetime.now().second))
            walker_prev_location = pedestrian(ego_vehicle, 1, walker_controller_bp, walker, world)
            walker_deter = True
            last_shown_pedestrain_time = datetime.now()
    
    # determine whether is hit 
    if (walker_deter):
        # walker_deter, walker_prev_location = walker_hit(walker, walker_deter, walker_prev_location)
        end_time = datetime.now()
        diff = (end_time - start_time).total_seconds()
        # if (not walker_deter and diff > 0.05): print("COLLIDE! total reaction time takes: ", diff, "secs")
        if (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_s]):
            print("user reaction time takes: ", diff, "secs")
            walker_deter = False
        if (diff > 0.75): # determine if user exceed certain threshold of inaction
            walker_deter = False
            print("user reaction time exceeds 0.75 secs")

    
    # Apply the control to the ego vehicle and tick the simulation
    ego_vehicle.apply_control(control)
    world.tick()

    # Update the display and check for the quit event
    pygame.display.flip()
    pygame.display.update()
    cv2.imshow("RGB_image", sensor_data['rgb_image'])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Sleep to ensure consistent loop timing
    clock.tick(60)