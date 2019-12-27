import os
import chess
import chess.engine
import cv2
import numpy as np

import board_color_calibration
import board_point_calibration
import board_warp_prespective_point
import chess_board_bool_value
import chess_board_mask
import chess_board_move_map
import conversion_fen_to_board

points = []    # contains chess board corners points
lower__w = []   # contains lower value for HSV of white player
upper__w = []   # contains upper  value for HSV of white player
lower__b = []   # contains lower value for HSV of black player
upper__b = []   # contains upper value for HSV of black player
boxes = np.zeros((8,8,4),dtype=int)    # contains top-left and bottom-right point of chessboard boxes 
required_contoures = []     # contains detected contors os players
required_contoures_mid_point = []   # contains mid-points of all detected contours
cnt_rect = []   # contains contours rectangle points
fen_line = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR' # fen line of chess board
board = chess.Board(fen=fen_line) # object of chess board
current_player_bool_position = [] # contains bool value of current player avablity
past_player_bool_position = [] # contains bool value of past player avablity
dir_path = os.path.dirname(os.path.realpath(__file__))+"/numpy_saved" # path of current directory
conversion_fen_to_board.fen2board(fen_line) # make sure that game starts with initial position 
chess_board = np.load(dir_path+"/ches_board.npz")["chess_board"]    # contains character value of player with position 
chess_board_past = [] # it contains past chess board player positions
prespective_flag = False # it shows true if we use image prespective
engine = chess.engine.SimpleEngine.popen_uci("Python_chess_intermediate_programs/stockfish-10-win/Windows/stockfish_10_x64.exe") # stockfish engine
chess_board_move_map.map_function()   # map dictonary key = board value to value = board box position
map_move = np.load(dir_path+"/map_position.npz")
# device = cv2.VideoCapture(0)
# _,img = device.read()

img = cv2.imread("Python_Chess_initial_programs/Images/first_step.jpeg")
# device = cv2.VideoCapture("http://192.168.1.136:4812/video")
# cv2.waitkey(100)
# ret , img = device.read()
# img  = img[582:582+1090,0:1078]
img = cv2.resize(img,(800,800))
# M = cv2.getRotationMatrix2D((img.shape[1]/2,img.shape[1]/2),270,1)
# img = cv2.warpAffine(img, M, img.shape[:2]) 
cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

if __name__ == "__main__":

    while True:
        print("do you want to warp prespective images [y/n]:",end=" ")
        ans = str(input())
        if ans == "y" or ans == "Y":
            print("==================================================")
            print("start warp prespective image:")
            print("press 'a' for get bottom-left point")
            print("press 'b' for get top-left point")
            print("press 'c' for get top-right point")
            print("press 'd' for get bottom-right point")
            print("press 'q' after calibrate points")
            board_warp_prespective_point.warp_prespective(img)
            pts1 = np.load(dir_path+'/chess_board_warp_prespective.npz')['pts1']
            pts2 = np.load(dir_path+'/chess_board_warp_prespective.npz')['pts2']
            matrix = cv2.getPerspectiveTransform(pts1,pts2)
            img = cv2.warpPerspective(img,matrix,(800,800))
            prespective_flag = True
            cv2.imshow("image",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print("Image warp prespective Done")
            print("==================================================")
            break
        elif ans == "n" or ans == "N":
            print("==================================================")
            while True:
                print("do you want to use saved warp prespective points [y/n] :",end=" ")
                answer = str(input())
                if answer == 'y' or answer == 'Y':
                    pts1 = np.load(dir_path+'/chess_board_warp_prespective.npz')['pts1']
                    pts2 = np.load(dir_path+'/chess_board_warp_prespective.npz')['pts2']
                    matrix = cv2.getPerspectiveTransform(pts1,pts2)
                    img = cv2.warpPerspective(img,matrix,(800,800))
                    prespective_flag = True
                    cv2.imshow("image",img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    print("done warp prespective of image with privously saved data")
                    print("==================================================")
                    break
                elif answer == 'n' or answer == 'N':
                    print("Ok , you want to use original image")
                    print("==================================================")
                    break
                else:
                    print("Enter Valid Input")
            break
        else:
            print("Enter Valid Input")

    while True:
        print("do you want to calibrate new Points [y/n]:",end=" ")
        ans = str(input())
        if ans == "y" or ans == "Y":
            board_point_calibration.get_points(img)
            points = np.load(dir_path+'/chess_board_points.npz')['points']
            break
        elif ans == "n" or ans == "N":
            # do some work
            print("==================================================")
            points = np.load(dir_path+'/chess_board_points.npz')['points']
            print("points Load successfully")
            print("==================================================")
            break
        else:
            print("==================================================")
            print("something wrong input")
            print("==================================================")

    while True:
        print("Do you want to calibrate color [y/n] :",end=" ")
        ans = str(input())
        if ans == "y" or ans == "Y":
            print("==================================================")
            print("calibration for white :")
            board_color_calibration.color_calibration(img,"w")
            lower__w =  np.load(dir_path+"/chess_w_color_points.npz")['lower']
            upper__w = np.load(dir_path+"/chess_w_color_points.npz")['upper']
            print("Done calibration for white")
            print("==================================================")
            print("calibration for black :")
            board_color_calibration.color_calibration(img,"b")
            lower__b =  np.load(dir_path+"/chess_b_color_points.npz")['lower']
            upper__b = np.load(dir_path+"/chess_b_color_points.npz")['upper']
            print("Done calibration for black")
            print("==================================================")
            break
        if ans == "n" or ans == "N":
            print("==================================================")
            lower__w =  np.load(dir_path+"/chess_w_color_points.npz")['lower']
            upper__w = np.load(dir_path+"/chess_w_color_points.npz")['upper']
            lower__b =  np.load(dir_path+"/chess_b_color_points.npz")['lower']
            upper__b = np.load(dir_path+"/chess_b_color_points.npz")['upper']
            print("color calibration successfully")
            print("==================================================")
            break
        else:
            print("==================================================")
            print("something wrong input")
            print("==================================================")
    

    # define Boxes
    for i in range(8):
        for j in range(8):
            # print(i,j)
            boxes[i][j][0] = points[i][j][0]
            boxes[i][j][1] = points[i][j][1]
            boxes[i][j][2] = points[i+1][j+1][0]
            boxes[i][j][3] = points[i+1][j+1][1]

    while True:
        print("==================================================")
        print("Do you want to see Boxex on Chess board [y/n]:",end=" ")
        ans = str(input())
        if ans == 'y' or ans == "Y":
            # show boxes
            img_box = img.copy()
            for i in range(8):
                for j in range(8):
                    box1 = boxes[i,j]
                    cv2.rectangle(img_box, (int(box1[0]), int(box1[1])), (int(box1[2]), int(box1[3])), (255,0,0), 2)
                    cv2.putText(img_box,"({},{})".format(i,j),(int(box1[2])-70, int(box1[3])-50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
                    cv2.imshow("img",img_box)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print("==================================================")
            break
        elif ans == 'N' or ans == "n":
            print("ok, got it you don't want ot see boxes")
            print("==================================================")
            break
        else:
            print("Enter valid input")

    np.savez(dir_path+"/chess_board_Box.npz",boxes=boxes)
    
    print("Start Game:")
    while not board.is_game_over():
        if board.turn:
            # white turn 

            # read image of chess board (it is not with calibration)
            # _,img = device.read()
            img = cv2.resize(img,(800,800))
            # if we have used ptespective points then flag will true else we are using original image 
            if prespective_flag:
                pts1 = np.load(dir_path+'/chess_board_warp_prespective.npz')['pts1']
                pts2 = np.load(dir_path+'/chess_board_warp_prespective.npz')['pts2']
                matrix = cv2.getPerspectiveTransform(pts1,pts2)
                img = cv2.warpPerspective(img,matrix,(800,800))
            
            # fen_line = conversion_fen_to_board.board2fen()
            result = engine.play(board, chess.engine.Limit(time=0.500))
            position1 = str(result.move)[0:2]
            position2 = str(result.move)[2:4]
            
            box_1_cordinate = map_move[position1]
            box_2_cordinate = map_move[position2]

            position1_box = boxes[box_1_cordinate[0]][box_1_cordinate[1]]
            position2_box = boxes[box_2_cordinate[0]][box_2_cordinate[1]]
            draw = img.copy() 
            cv2.rectangle(draw,(position1_box[0],position1_box[1]),(position1_box[2],position1_box[3]),(0,0,255),3)
            cv2.rectangle(draw,(position2_box[0],position2_box[1]),(position2_box[2],position2_box[3]),(0,255,0),3)
            cv2.imshow("Game",draw)
            print("player :",chess_board[box_1_cordinate[0]][box_1_cordinate[1]],"\nmoves from : ",position1,"\nmoves to : ",position2)
            board.push(result.move)
            cv2.waitKey(0)

        else:
            # balck turn

            ################################################################
            ## if there are no one to play chess
            ################################################################

            result = engine.play(board, chess.engine.Limit(time=0.400))
            position1 = str(result.move)[0:2]
            position2 = str(result.move)[2:4]
            
            box_1_cordinate = map_move[position1]
            box_2_cordinate = map_move[position2]

            position1_box = boxes[box_1_cordinate[0]][box_1_cordinate[1]]
            position2_box = boxes[box_2_cordinate[0]][box_2_cordinate[1]]
            draw = img.copy() 
            cv2.rectangle(draw,(position1_box[0],position1_box[1]),(position1_box[2],position1_box[3]),(0,0,255),3)
            cv2.rectangle(draw,(position2_box[0],position2_box[1]),(position2_box[2],position2_box[3]),(0,255,0),3)
            cv2.imshow("Game",draw)

            print("player :",chess_board[box_1_cordinate[0]][box_1_cordinate[1]],"\nmoves from : ",position1,"\nmoves to : ",position2)
            # print(board)
            board.push(result.move)
            cv2.waitKey(0)

            ################################################################
            ## Opponent id real player
            ################################################################

            # img = cv2.imread("")
            # device = cv2.VideoCapture("http://192.168.1.136:4812/video")
            # ret , img = device.read()
            # img  = img[582:582+1090,0:1078]
            # img = cv2.resize(img,(800,800))

            # past_player_bool_position = chess_board_bool_value.convert_to_bool(img)
            # print("past palyer bool position :",past_player_bool_position)
            # chess_board_past = conversion_fen_to_board.fen2board(board.fen())

            # # it's time of player to move
            # print("Player's Turn :")
            # print("Press 'a' when player complete move : ")
            # while True:
            #     k = cv2.waitKey(1)
            #     if k == ord('a'):
            #         break

            # # img = cv2.imread("")
            # device = cv2.VideoCapture("http://192.168.1.136:4812/video")
            # ret , img = device.read()
            # img  = img[582:582+1090,0:1078]
            # img = cv2.resize(img,(800,800))

            # current_player_bool_position = chess_board_bool_value.convert_to_bool(img)
            # print("current Player Position : ",current_player_bool_position)
            # difference = past_player_bool_position - current_player_bool_position
            # print("Differenc : ",difference)

            # position_of_negative = np.where(difference==-1)
            # position_of_positive = np.where(difference==1)
            # print("Position of negative :",position_of_negative)
            # print("Positon of positive : ",position_of_positive)
            # chess_board = chess_board_past
            # player_moved = chess_board_past[position_of_negative[0]][position_of_negative[1]]
            # chess_board[position_of_negative] = '1'
            # chess_board[position_of_positive] = player_moved
            # np.savez(dir_path+"/ches_board.npz",chess_board = chess_board)
            # fen_line = conversion_fen_to_board.board2fen()
            # # board.push(move) add is better idea
            # board = chess.Board(fen=fen_line)
            # print("after Player move Board Position :")
            # chess_board =  conversion_fen_to_board.fen2board(board.fen())
            # print(chess_board)
