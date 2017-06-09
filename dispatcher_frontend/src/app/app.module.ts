import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule } from '@angular/http';
import { FormsModule }   from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';

import { AuthGuard } from './guard/auth.guard';

import { LoginComponent } from './login/login.component';
import { NavigationBarComponent } from './navigation-bar/navigation-bar.component'
import { DashboardModule } from './dashboard/dashboard.module';
import { TasksComponent } from './tasks/tasks.component';
import { TaskDetailComponent } from './tasks/task-detail.component';
import { NodesComponent } from './nodes/nodes.component';
import { TaskService } from './model/task.service';

import { AuthService } from './service/auth.service';


@NgModule({
    imports: [ 
        BrowserModule, 
        AppRoutingModule,
        HttpModule,
        FormsModule,
        NgbModule.forRoot(),
        DashboardModule
    ],
    declarations: [ 
        AppComponent, 
        LoginComponent,
        NavigationBarComponent,
        TasksComponent, 
        TaskDetailComponent,
        NodesComponent
    ],
    providers: [
        AuthService,
        AuthGuard,
        TaskService
    ],
    bootstrap: [ AppComponent ]
})
export class AppModule { }
