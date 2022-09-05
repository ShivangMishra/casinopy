import pickle
import bpy
import math
import sys

# disk_speeds = []
# disk_times = [5, 8, 10, 12]  # in seconds

INITIAL_NUM_AT_BOTTOM = 5
N_DISKS = 4
N_SECTIONS = 10  # Number of sections in one disk
FPS = 24
START_FRAME = 1
END_FRAME = 200
DEGREES_PER_FRAME = 15  # for 360 degrees per second

disk_names = ['disk1', 'disk2', 'disk3', 'disk4']
ball_names = ['ball1', 'ball2', 'ball3', 'ball4']
num_names = [
    ['num11', 'num12', 'num13', 'num14'],
    ['num21', 'num22', 'num23', 'num24'],
    ['num31', 'num32', 'num33', 'num34'],
    ['num41', 'num42', 'num43', 'num44']
]

show = [
    [6.8843, 1.6267, 1.8191],  # x,y,z
    [7.1357, 1.1749, 1.8191],
    [7.3851, 0.72693, 1.8191],
    [7.6484, 0.25381, 1.8191]
]
hidex = 8.5108
hidey = 0.765
hidez = 0.809


def num_to_section(num, init_num_at_bottom=5):
    if num <= INITIAL_NUM_AT_BOTTOM:
        return INITIAL_NUM_AT_BOTTOM - num

    else:
        return N_SECTIONS + INITIAL_NUM_AT_BOTTOM - num


def angle_to_degree(angle):
    return angle // 36


def section_to_angle(section):
    return 36 * section


def init_nums(all_nums):
    for i in range(4):
        for j in range(4):
            num_ob = bpy.context.scene.objects[num_names[i][j]]
            num_ob.data.body = str(all_nums[i][j])
            num_ob.location.x = hidex
            num_ob.location.y = hidey
            num_ob.location.z = hidez


def show_nums(round, frame_start, frame_end):
    names = num_names[round]
    for i in range(len(names)):
        num_ob = bpy.context.scene.objects[num_names[round][i]]
        num_ob.keyframe_insert(data_path='location', frame=frame_start)
        num_ob.location.x = show[i][0]
        num_ob.location.y = show[i][1]
        num_ob.location.z = show[i][2]
        num_ob.keyframe_insert(data_path='location', frame=frame_end)
    if round == 0:
        return

    for i in range(len(num_names[round-1])):
        num_ob = bpy.context.scene.objects[num_names[round-1][i]]
        num_ob.keyframe_insert(data_path='location', frame=frame_start)
        num_ob.location.x = hidex
        num_ob.location.y = hidey
        num_ob.location.z = hidez
        num_ob.keyframe_insert(data_path='location',
                               frame=(frame_end+frame_start)//2 + 1)
    pass


def add_anims(disk_nums, disk_times, disk_speeds, initFrame=0):
    max_frames = 0
    for i in range(N_DISKS):
        name = disk_names[i]
        num = disk_nums[i]

        nframes = FPS * disk_times[i]
        max_frames = max(max_frames, nframes)
        dpf = disk_speeds[i]/FPS
        rotation = math.radians(nframes * dpf)

        disk = bpy.context.scene.objects[name]       # Get the disk
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
        bpy.context.view_layer.objects.active = disk   # Make the disk the active object
        disk.select_set(True)

        final_rotation = disk.rotation_euler[1] + rotation  # IN Radians
        # IN DEGREES
        final_rotation_deg = disk.rotation_euler[1] * 180 + nframes * dpf

        final_rotation_principal = final_rotation_deg % 360  # 0 to 360

        req_section = num_to_section(num)
        req_angle_deg = section_to_angle(req_section)

        diff_deg = req_angle_deg - final_rotation_principal

        diff_rad = math.radians(diff_deg)
        final_rotation += diff_rad

        # if disk.animation_data:  # Check for presence of animation data.
        #     disk.animation_data.action = None

        # if disk.animation_data and disk.animation_data.nla_tracks:
        #     for nt in disk.animation_data.nla_tracks:
        #         disk.animation_data.nla_tracks.remove(nt)

        # if disk.animation_data and disk.animation_data.drivers:
        #     for dr in disk.animation_data.drivers:
        #         disk.animation_data.drivers.remove(dr)

        disk.keyframe_insert(data_path='rotation_euler', frame=initFrame)
        disk.rotation_euler = [disk.rotation_euler[0],
                               final_rotation, disk.rotation_euler[2]]
        disk.keyframe_insert(data_path='rotation_euler',
                             frame=initFrame + nframes)
    return initFrame + max_frames


def reset_rotation(start_frame, end_frame):
    for i in range(N_DISKS):
        name = disk_names[i]
        disk = bpy.context.scene.objects[name]       # Get the disk
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
        bpy.context.view_layer.objects.active = disk   # Make the disk the active object
        disk.select_set(True)
        disk.keyframe_insert(data_path='rotation_euler', frame=start_frame)
        disk.rotation_euler = [disk.rotation_euler[0],
                               0, disk.rotation_euler[2]]
        disk.keyframe_insert(data_path='rotation_euler', frame=end_frame)


def all_rounds(rounds):
    next_frame = 0
    delay = 2 * FPS
    all_nums = [round['nums'] for round in rounds]
    init_nums(all_nums)
    for rIdx, round in enumerate(rounds):
        nums = round['nums']
        times = round['times']
        speeds = round['speeds']

        next_frame = add_anims(nums, times, speeds,
                               next_frame)
        reset_rotation(next_frame + delay, next_frame + 2*delay)
        show_nums(round=rIdx, frame_start=next_frame +
                  delay, frame_end=next_frame + 2*delay)
        next_frame += 3*delay
    return next_frame


def render_video(frame_start, frame_end, filepath, resolution):
    # perhaps set resolution in code
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end

    rnd = bpy.context.scene.render
    rnd.filepath = filepath
    # rnd.resolution_x = resolution['x']
    # rnd.resolution_y = resolution['y']
    rnd.resolution_percentage = 50
    bpy.ops.render.render(animation=True)


# argv = sys.argv
# argv = argv[argv.index("--") + 1:]
config = {}
with open("myconfig", 'rb') as f:
    config = pickle.load(f)

last_frame = all_rounds(config)

# render_video(0, last_frame, "C:\\Users\\shiva\\rendered_video\\render_video",
#              {'x': 640, 'y': 480})
