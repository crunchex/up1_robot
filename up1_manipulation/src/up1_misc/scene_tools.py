import rospy
from moveit_commander import PlanningSceneInterface
from moveit_msgs.msg import PlanningScene, ObjectColor


class Scene:
    def __init__(self):
        self.pub = rospy.Publisher('planning_scene', PlanningScene, queue_size=10)
        self.interface = PlanningSceneInterface()

        self.colors = dict()

    def clear_all(self):
        self.interface.remove_world_object(name='')

    def add_target(self, target):
        self.interface.add_box(target.id, target.get_initial_pose(), target.size)

    def add_rig(self, rig):
        self.interface.add_mesh(rig.id, rig.get_initial_pose(), rig.get_stl_path(), rig.scale_tuple)

    # Set the color of an object by rgba values
    def set_color(self, obj, r, g, b, a=0.9):
        color = ObjectColor()
        color.id = obj.id

        # Set the rgb and alpha values given as input
        color.color.r = r
        color.color.g = g
        color.color.b = b
        color.color.a = a

        # Update the global color dictionary
        self.colors[obj.id] = color

    # Set the color of an object by name
    def set_color_by_name(self, obj, color_str):
        color_names = {
            'yellow': [0, 0, 1.0, 1.0],
            'blue': [0.9, 0.9, 0, 1.0]
        }

        color_rgba = color_names[color_str]
        self.set_color(obj, color_rgba[0], color_rgba[1], color_rgba[2], color_rgba[3])


    # Actually send the colors to MoveIt!
    def send_colors(self):
        # Initialize a planning scene object
        p = PlanningScene()

        # Need to publish a planning scene diff
        p.is_diff = True

        # Append the colors from the global color dictionary
        for color in self.colors.values():
            p.object_colors.append(color)

        # Publish the scene diff
        self.pub.publish(p)