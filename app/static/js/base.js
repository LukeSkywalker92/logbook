var path = window.location.pathname.split('/')

path.pop()
path.shift()

var navLink = document.getElementById('nav-link');
var link = '';
var a = document.createElement('a');
a.href = '/';
a.innerHTML = 'home';
a.classList = 'menu-item';
navLink.appendChild(a);

for (var p in path) {
    link += '/'+path[p];
    var a = document.createElement('a');
    a.href = link;
    a.innerHTML = '/'+path[p];
    a.classList = 'menu-item';
    navLink.appendChild(a);
}