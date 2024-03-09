import { RcFile } from 'antd/es/upload';
import { makeAutoObservable } from 'mobx';
import { Dependency, ProjectInfo, ProjectTask } from '../api/models/Project';
import { Task } from 'gantt-task-react';

export class RootStore {
    projectInfo: ProjectInfo | null = null;
    uploadedGanttTasks: Task[] | null = null;

    constructor() {
        makeAutoObservable(this);
    }

    uplaodFile(file: RcFile) {
        if (file) {
            const reader = new FileReader();

            reader.onload = () => {
                try {
                    const parsedData = JSON.parse(reader.result as string);
                    this.projectInfo = parsedData;

                    if (this.projectInfo) {
                        this.uploadedGanttTasks = this.addDependenciesToTasks(
                            this.mapProjectInfoToTasks(this.projectInfo.tasks.rows),
                            this.projectInfo.dependencies.rows
                        );

                        console.log('Gantt tasks:', this.uploadedGanttTasks);
                    }
                } catch (error) {
                    console.error('Error parsing JSON:', error);
                }
            };

            reader.readAsText(file);
        }
    }

    mapProjectInfoToTasks(tasks: ProjectTask[]): Task[] {
        const mappedTasks: Task[] = [];

        tasks.forEach((task) => {
            if (task.children && task.children.length > 0) {
                const mappedChildren = this.mapProjectInfoToTasks(task.children);

                mappedTasks.push({
                    id: task.id,
                    type: 'project',
                    name: task.name,
                    start: new Date(task.startDate),
                    end: new Date(task.endDate),
                    progress: task.percentDone,
                    isDisabled: task.inactive,
                    project: task.parentId,
                    dependencies: [],
                    hideChildren: false,
                });

                mappedTasks.push(...mappedChildren);
            } else {
                mappedTasks.push({
                    id: task.id,
                    type: 'task',
                    name: task.name,
                    start: new Date(task.startDate),
                    end: new Date(task.endDate),
                    progress: task.percentDone,
                    isDisabled: task.inactive,
                    project: task.parentId,
                    dependencies: [],
                    hideChildren: false,
                });
            }
        });

        return mappedTasks;
    }

    addDependenciesToTasks(tasks: Task[], dependencies: Dependency[]): Task[] {
        tasks.forEach((task) => {
            const taskDependencies = dependencies.filter((dependency) => dependency.to === task.id);
            taskDependencies.forEach((dependency) => {
                const dependentTask = tasks.find((t) => t.id === dependency.from);
                if (dependentTask) {
                    task.dependencies?.push(dependentTask.id);
                }
            });
        });

        return tasks;
    }
}
