<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{{firstName}}'s Portfolio</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
        <link rel="stylesheet" href="../Scripts/index.css">
        <link rel="shortcut icon" href="/Images/logo-betters.png">
        
    </head>
    <header>
        <nav class="navbar navbar-expand-lg navbar-custom fixed-top sticky-top bg-dark">
            <h3 class="navbar-brand float-md-start mb-0">{{fullName}}</h3>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarContent" aria-controls="navbarContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarContent">
                <ul class="navbar-nav mr-auto nav-fill">
                    <li class="nav-item active">
                        <a class="nav-link" href="./">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="./about-me">About me</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="./project">Projects</a>
                    </li>
                </ul>
                <form class="d-flex" role="search" method="POST" action="./SearchProject">
                    <input class="form-control me-2" name="SearchBox" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form>
            </div>
        </nav>
    </header>
    <body>
        
    <div class="site-wrapper">
        <div class="inner cover">
            <h1>{{fullName}}</h1> <br>
            <div class="row" style="width: 50%; margin: 0 auto;">
                <div class="col-xs-4">
                    <h3>Education</h3>
                    <p>{{schoolName}}</p>
                    <p>{{majorName}}</p>
                </div>
                <div class="col-xs-4">
                    <h3>Certifications</h3>
                    {{!certifications}}
                </div>
                <div class="col-xs-4" style="width: 50%; margin: 0 auto;">
                    <h3>Skills</h3>
                    {{!skills}}
                </div>
            </div>
            
        </div>
  
      </div>
        
    </body>
    <footer class="mt-auto text-white-50 bg-dark">
                <h4>Contact Me: 
                  <a href="{{githubLink}}"><svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-github" viewBox="0 0 16 16">
                  <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                </svg></a> 
                <a href="mailto:{{email}}"><svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-envelope-fill" viewBox="0 0 16 16">
                  <path d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414.05 3.555ZM0 4.697v7.104l5.803-3.558L0 4.697ZM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586l-1.239-.757Zm3.436-.586L16 11.801V4.697l-5.803 3.546Z"/>
                </svg></a></h4>
              </footer>
</html>