import random

m=1
b=1
roomNumberUpOriginal = 3
roomNumberDownOriginal = 3
roomNumberUpLeft = roomNumberUpOriginal
roomNumberDownLeft = roomNumberDownOriginal

task = -1
completedTasks = []
availableTasks = [0, 1*m, 2*b]
side = 0 #side to work with (0->up, 1->down)
for r in range(roomNumberUpOriginal + roomNumberDownOriginal + b + m):
 # let's decide randomly what's next (0->office room, 1->meeting, 2->bathroom)
 # if last task was 0 ad there are rooms left, next task will be 0 again
 # completedTasks 1 and 2 cannot be done twice in the same side AND environment
 if side == 0:
    if task == 0 and roomNumberUpLeft > 0:
       completedTasks.append(0)
       roomNumberUpLeft -= 1
    elif len(completedTasks) == max(roomNumberUpOriginal + b, roomNumberUpOriginal + m):
       side = 1
    else:
       while True:
          r = random.choice(availableTasks)
          if r not in completedTasks:
            if (r == 1 and 2 not in completedTasks) or (r == 2 and 1 not in completedTasks):
               task = r
               completedTasks.append(task)
               break
            elif r == 0 and roomNumberUpLeft > 0:
               task = r
               completedTasks.append(task)
               roomNumberUpLeft -= 1
               break
 if side == 1:
    if task == 0 and roomNumberDownLeft > 0:
       completedTasks.append(0)
       roomNumberDownLeft -= 1
    elif len(completedTasks) == roomNumberUpOriginal + roomNumberDownOriginal + b + m:
       side = -1
    else:
       while True:
          r = random.choice(availableTasks)
          if (r not in completedTasks):
             task = r
             completedTasks.append(task)
             break
          elif (r == 0 and roomNumberDownLeft > 0):
             task = r
             completedTasks.append(task)
             roomNumberDownLeft -= 1
             break
 if side >= 0:
    print("Side %", side)
    print("Disponibles: %",availableTasks)
    print("Elegida: %",task)
    print("Completadas: %",completedTasks)
    print("------------------------------------")
print("fin")