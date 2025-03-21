var script = document.createElement("script");
script.src = "http://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js";
script.type = "text/javascript";
var script1 = document.createElement("script");
script1.src = "https://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js";
script1.type = "text/javascript";
document.getElementsByTagName("head")[0].appendChild(script1);
document.getElementsByTagName("head")[1].appendChild(script);
var people = [];
    availableCommands = $.getJSON('../information/limitedshell.json', function(data) {
        availableCommands = data.availableCommands;
    });
    Commands = $.getJSON('../information/limitedshell.json', function(seconddata) {
        Commands = seconddata.commands;
    });
    count = 0;
    sshcount = 0;
    sshtries = 0;
    inssh = false;
    gamerun = true;
    site = ""
    sites = ["credentials.garfield.com", "aboutme.garfield.com", "projects.garfield.com"];

    function getPasswords(){
        credentials = {};
        for (let i = 0; i < Commands["passwords.txt"].split("\n").length; i++){
            site = Commands["passwords.txt"].split("\n")[i].split("@")[1].split(":")[0];
            password = Commands["passwords.txt"].split("\n")[i].split(":")[1];
            credentials[site] = password;
        }
        return credentials;
    }

    function getUserInput(command){
        if (event.key === 'Enter'){
            if (gamerun){
                if (command.value != ''){
                    var output = Execute(command.value);
                    if (output !== -1){
                        UpdateContent(output, command.value);
                    }
                }
            }
        }
    }
    
    function sshgetUserInput(command){
        if (event.key === 'Enter'){
            if (gamerun){
                if (command.value != ''){
                    var output = sshExecute(command.value);
                    if (inssh){
                        if (output !== -1){
                            sshUpdateContent(output, command.value, site);
                        }
                    }
                    else {
                        result = "Connection shutdown by user"
                        document.getElementById("result"+count).textContent=result; 
                        //---- Removes the function call in the text ----
                        document.getElementById("text"+count).innerHTML='<p class="hostname">garfield@'+site+'$<span>'+command+'</span></p>';
                        const GameContent = document.getElementById("terminalgame");
                        count+=1;
                        GameContent.insertAdjacentHTML('beforeend', '<div id="text'+count+'"><p class="hostname">garfield@'+site+'$<input type="text" id="text" onkeydown="getUserInput(this)" autofocus></p></div><p class="result" id="result' + count +'"></p>');
                    }
                }
            }
        }
    }

    function Execute(FullCommand){
        Command = FullCommand.split(" ")[0];
        if (availableCommands.indexOf(Command) !== -1){
            if (Command.indexOf("echo") !== -1){
                return FullCommand.split(" ").slice(1,FullCommand.split(" ").length);
            }
            else if (Command.indexOf("exit") !== -1){
                gamerun = false;
                return "Shutting Down";
            }
            if (FullCommand.split(" ").length == 2){
                if (Command.indexOf("cat") !== -1){
                    return Commands[FullCommand.split(" ")[1]];
                }
                else if (Command.indexOf("dig") !== -1 || Command.indexOf("nslookup") !== -1  || Command.indexOf("msfvenom") !== -1 ){
                    return Commands[FullCommand.split(" ")[1].split(".")[0] + Command];
                }
                else {
                    passwordcredentials = getPasswords()
                    if (sites.indexOf(FullCommand.split(" ")[1].split("@")[1]) !== -1){
                        site = FullCommand.split(" ")[1].split("@")[1];
                        sshinput(site)
                        return -1;
                    }
                }
            }
            else {
                return Commands[Command];
            }
        }
        else {
            return `bash: ${Command}: Command not found`;
        }
    }

    function sshExecute(FullCommand){
        Command = FullCommand.split(" ")[0];
        if (availableCommands.indexOf(Command) !== -1){
            console.log("valid command")
            if (Command.indexOf("echo") !== -1){
                return FullCommand.split(" ").slice(1,FullCommand.split(" ").length);
            }
            else if (Command.indexOf("exit") !== -1){
                inssh = false;
            }
            else if (Command.indexOf("pwd") !== -1 || Command.indexOf("sudo") !== -1  || Command.indexOf("whoami") !== -1 ){
                return Commands[Command];
            }
            if (FullCommand.split(" ").length == 2){
                if (Command.indexOf("dig") !== -1 || Command.indexOf("nslookup") !== -1  || Command.indexOf("msfvenom") !== -1){
                    return Commands[Command];
                }
                else if (Command.indexOf("cat") !== -1){
                    if (Commands[site+FullCommand.split(" ")[1]] != NaN){
                        return Commands[site.split(".")[0]+FullCommand.split(" ")[1]]
                    }
                    else {
                        return `cat: ${FullCommand.split(" ")[1]}: No such file or directory`
                    }
                }
                else {
                    console.log("ssh")
                }
            }
            else {
                if (FullCommand.split(" ").length == 1){
                    console.log("here")
                    console.log(site.split(".")[0]+FullCommand.split(" ")[0])
                    return Commands[site.split(".")[0]+FullCommand.split(" ")[0]]
                }
            }
            
        }
    }

    function sshinput(site){
        const GameContent = document.getElementById("terminalgame");
        console.log(site)
        GameContent.insertAdjacentHTML('beforeend', '<div id="ssh'+sshcount+'"><p class="hostname">garfield@'+site+' Password: <input type="text" id="text" onkeydown="sshpassword(this,\''+site+'\')" autofocus></p></div>')
        sshcount+=1;
    }

    function sshpassword(password,site){
        if (event.key === "Enter") {
            if (sshtries < 2){
                if (password.value.trim() == passwordcredentials[site]){
                    const GameContent = document.getElementById("terminalgame");
                    GameContent.insertAdjacentHTML('beforeend', '<p class="result" id="sshresult' + sshcount +'">Connected to '+ site + '</p>');
                    sshtries = 0;
                    inssh = true;
                    count+=1;
                    site = site
                    const GameContent1 = document.getElementById("terminalgame");
                    GameContent1.insertAdjacentHTML('beforeend', '<div id="text'+count+'"><p class="hostname">garfield@'+site+'$<input type="text" id="text" onkeydown="sshgetUserInput(this)" autofocus></p></div><p class="result" id="result' + count +'"></p>');
                }
                else {
                    document.getElementById("ssh"+(sshcount-1)).innerHTML='<p class="hostname">garfield@'+site+' Password: <span>'+password.value.trim()+'</span></p>';
                    sshinput(site)
                    //console.log(sshtries)
                    sshtries+=1;
                }
            }
            else {
                count+=1;
                site="garfieldPortfolio";
                const GameContent = document.getElementById("terminalgame");
                GameContent.insertAdjacentHTML('beforeend', '<div id="text'+count+'"><p class="hostname">garfield@'+site+'$<input type="text" id="text" onkeydown="getUserInput(this)" autofocus></p></div><p class="result" id="result' + count +'"></p>');
            }
            
        }
            
        
    }

    function UpdateContent(ele, command) {
            //alert(ele.value); 
            site="garfieldPortfolio";
            result = ele;
            //---- Increments the result and text -----
            document.getElementById("result"+count).textContent=result; 
            //---- Removes the function call in the text ----
            document.getElementById("text"+count).innerHTML='<p class="hostname">garfield@'+site+'$<span>'+command+'</span></p>';
            count+=1;  
            //---- Creates the next input and result ----
            const GameContent = document.getElementById("terminalgame");
            if (gamerun){
                GameContent.insertAdjacentHTML('beforeend', '<div id="text'+count+'"><p class="hostname">garfield@'+site+'$<input type="text" id="text" onkeydown="getUserInput(this)" autofocus></p></div><p class="result" id="result' + count +'"></p>');
            }
        }
    
        function sshUpdateContent(ele, command, site) {
            //alert(ele.value); 
            site=site;
            result = ele;
            //---- Increments the result and text -----
            document.getElementById("result"+count).textContent=result; 
            //---- Removes the function call in the text ----
            document.getElementById("text"+count).innerHTML='<p class="hostname">garfield@'+site+'$<span>'+command+'</span></p>';
            count+=1;  
            //---- Creates the next input and result ----
            const GameContent = document.getElementById("terminalgame");
            if (inssh){
                GameContent.insertAdjacentHTML('beforeend', '<div id="text'+count+'"><p class="hostname">garfield@'+site+'$<input type="text" id="text" onkeydown="sshgetUserInput(this)" autofocus></p></div><p class="result" id="result' + count +'"></p>');
            }
        }