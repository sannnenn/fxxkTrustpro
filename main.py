from time import sleep

import autoPilot


ap = autoPilot.autoPilot()
ap.login()
ap.openWeeklyReport()
ap.setWeekReport()



#sleep(60)