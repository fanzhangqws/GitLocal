process1: get data from jfcrm and store all Changqing order to servicechange database
process2: read servicechange database order and send orders to Changqing
process3: set finish flag for chinatelecom's database
process4: read finishing status from Changqing FTP server and set servicechange database finish status to what have written at FTP server
process5: make a website to display order serialuserid and the respective finish status