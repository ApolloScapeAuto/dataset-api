1. prediction_train.zip: Trainning data for trajectory prediction. 
    Each file is a 1min sequence with 2fps. 
    Each line in every file contains frame_id, object_id, object_type, position_x, position_y, position_z, object_length, object_width, object_height, heading. 
    For object_type, 1 for small vehicles, 2 for big vehicles, 3 for pedestrian, 4 for bicyclist and 5 for others. We consider the first two types as one type (vehicles) in this challenge.
    Position is in the world coordinate system. We just think the traffic in a 2D plane and ignore its position_z.
    The unit for the position and bounding box is meter.
    The heading value is the steering radian with respect to the direction of the object. 
    You do not need to use all the info we provide. The output of your prediction is just the position_x and position_y in the next several seconds.
    
2. prediction_test.zip: Testing data for trajectory prediction. 
    Each line in the prediction_test.txt contains frame_id, object_id, object_type, position_x, position_y. 
    Each six frames in the prediction_test.txt is a testing sequence. Each sequence is independent. You need read the file carefully.