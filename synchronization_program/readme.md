## Sync program 

### Purpose

Sync a main folder with a replica. 

### Overlook 

<img width="627" alt="Screenshot 2023-07-27 at 12 10 24" src="https://github.com/StefanIancu/projects/assets/124818078/cc10741a-1dac-42f6-9758-b167cce91ca3">

Once the program is started, the source and the date is logged through the console and through the log.log file. 

<img width="431" alt="Screenshot 2023-07-27 at 12 10 58" src="https://github.com/StefanIancu/projects/assets/124818078/27fddb3c-0a78-4bdb-a044-93d78bd94961">

When the program is running, if a file is created it will be automatically copied to the replica folder. 
Every entry will be logged as well on the console and into log.log. 

<img width="317" alt="Screenshot 2023-07-27 at 12 11 11" src="https://github.com/StefanIancu/projects/assets/124818078/a4565bac-1411-462c-b601-2fa4eaef3cc6">

If a file is deleted from the source directory, the program will automatically detect which file was deleted, log the info to console and log.log and will delete the file from the replica program as well. 

### Extras

The program is now set to run in a loop executing the syncing almost instantly (2 sec). This can be changed anytime. 

### Further implements

The program could be converted into an executable file and scheduled to run at certain times from the console/terminal. 
