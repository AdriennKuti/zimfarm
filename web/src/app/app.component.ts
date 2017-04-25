import { Component } from '@angular/core';

@Component({
    selector: 'zimfarm',
    templateUrl: 'app/app.component.html'
})
export class AppComponent {
    tabs = [
        {name: "Dashboard", routerLink: "dashboard"},
        {name: "Tasks", routerLink: "tasks"},
        {name: "Templates", routerLink: "templates"},
        {name: "Nodes", routerLink: "nodes"}
    ]
}
