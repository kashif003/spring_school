from recorded_positions import pickup_coordinates,dropoff_coordinates

def get_pickup_coordinates(p):
    return pickup_coordinates.get(p,'Invalid_position')
def get_dropoff_coordinates(p):
    return dropoff_coordinates.get(p,'Invalid_position')

def go_up(position_coordinates):
    coordinates=[0,0,0.03 ,0,0,0]
    result = [a + b for a, b in zip(position_coordinates, coordinates)]
    robot.arm.move_pose(result)

def go_down(position_coordinates):
    coordinates=[0,0,0.03 ,0,0,0]
    result = [a + b for a, b in zip(position_coordinates, coordinates)]
    robot.arm.move_pose(result)

def clear_space(played_positions_robot,played_positions_player):
    robot_storage_positions=['c1','c2','c3','c4','c5']
    player_storage_positions=['c6','c7','c8','c9','c10']

    for i in range(len(played_positions_robot)):
        robot.arm.move_pose(get_pickup_coordinates(played_positions_robot(i)))
        robot.tool.grasp_with_tool()
        go_up(get_pickup_coordinates(played_positions_robot(i)))

        go_down(get_dropoff_coordinates(robot_storage_positions(i)))
        robot.arm.move_pose(get_dropoff_coordinates(robot_storage_positions(i)))
        robot.tool.release_with_tool()

    for i in range(len(played_positions_player)):
        robot.arm.move_pose(get_pickup_coordinates(played_positions_player(i)))
        robot.tool.grasp_with_tool()
        go_up(get_pickup_coordinates(played_positions_player(i)))

        go_down(get_dropoff_coordinates(player_storage_positions(i)))
        robot.arm.move_pose(get_dropoff_coordinates(player_storage_positions(i)))
        robot.tool.release_with_tool()

    robot.arm.move_pose(get_dropoff_coordinates('h0'))

    

    






    