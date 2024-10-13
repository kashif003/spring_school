def movement(postions_robot,positions_player=0,clear_out=False):
         if clear_out==False:
            if pickup_index <= 4:
                 robot.arm.move_pose(get_pickup_coordinates(pick_up_list[pickup_index]))
                 robot.tool.grasp_with_tool()
                 go_up(get_pickup_coordinates(pick_up_list[pickup_index]))

                 go_down(get_dropoff_coordinates(postions_robot[0]))
                 robot.arm.move_pose(get_dropoff_coordinates(postions_robot[0]))
                 robot.tool.release_with_tool()
                
                 robot.arm.move_pose(get_dropoff_coordinates('h0'))    # check this line 
            
                 pickup_index+=1

         else:  
                concatenated_list = postions_robot + positions_player

                for i in range(len(concatenated_list)):
                     robot.arm.move_pose(get_pickup_coordinates(concatenated_list[i]))
                     robot.tool.grasp_with_tool()
                     go_up(get_pickup_coordinates(concatenated_list[i]))

                     go_down(get_dropoff_coordinates(pick_up_list[i]))

                     robot.arm.move_pose(get_dropoff_coordinates(pick_up_list[i]))
                     robot.tool.release_with_tool()
                     robot.arm.move_pose(get_dropoff_coordinates('h0'))
