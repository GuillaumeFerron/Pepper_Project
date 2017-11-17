 Pepper Project :
 
 pour lancer une démo pepper : 
 se brancher en filaire pour avoir une bonne adresse IP et testere un ping : ping 134.214.220.7 (adresse pepper)
 
 - si ping marche faire une connection ssh avec port forwarding dans les deux sens : 
 ssh nao@134.214.220.7 -v -N -L 9559:127.0.0.1:9559 -R 11311:127.0.0.1:11311
 
s'authentifier avec le mdp : amelie

- une fois connecté lancer : roslaunch pepper_bringup pepper_full.launch network_interfaces:=lo
- source catkin_pepper_ws/devel/setup.bash
- lancer dans une autre fenêtre du terminal :rviz rviz -d utils/pepper.rviz
- pour teleopérer pepper :
  * ls /dev/input pour vérifier quel device est connecté 
  *connecter la manette ps avec la prise usb 
  * ls /dev/input pour vérifier si la manette est sur js1 ou js0
  * sudo chmod a+rw /dev/input/jsX
  pour vérifier que la manette marche
  * rosparam set jy_node/dev "/dev/input/jsX"
  * rosrun joy joy_node
  * rostopic echo joy 
  Si tout se passe bien, les informations du topic joy devraient changer en fonction des touches pressées.
  Une fois le test réalisé il faut s'assurer que le bon device match le fichier launch du teleop
  *ouvrir le fichier : catkin_pepper_ws/src/pepper-ros-teleop/launch/pepper_ps3_teleop.launch
  *vérifier que le device est le bon numero dans le mapping du parametre du noeud joy.
  Une fois vérifié, le reste peut être lancé (si cela ne marche pas il faut resourcer le fichier setup.bash):
- roslaunch pepper_teleop pepper_ps3_teleop.launch
Enfin pour que pepper soit commandable il faut : 
- que le pepper ne soit pas branché au secteur
- lancer le script du fixant la limite interne du pepper : python utils/fix_behaviour.py
- lancer le script obstacle avoidance : python catkin_pepper_ws/src/pepper_navigation/scripts/obstacle_avoidance.py
  
  
