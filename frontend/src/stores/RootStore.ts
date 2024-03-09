import { RcFile } from 'antd/es/upload';
import { makeAutoObservable } from 'mobx';
import { Dependency, ProjectInfo, ProjectTask } from '../api/models/Project';
import { Task } from 'gantt-task-react';

export class RootStore {
    projectInfo: ProjectInfo | null = null;
    ganttTasks: Task[] | null = null;

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
                        this.ganttTasks = this.addDependenciesToTasks(
                            this.mapProjectInfoToTasks(this.projectInfo.tasks.rows),
                            this.projectInfo.dependencies.rows
                        );

                        console.log('Gantt tasks:', this.ganttTasks);
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
            // Check if the task has children
            if (task.children && task.children.length > 0) {
                // Recursively call the function for each child
                const mappedChildren = this.mapProjectInfoToTasks(task.children);
                // Add the children to the mappedTasks array
                mappedTasks.push(...mappedChildren);
            } else {
                // If the task has no children, add it to the mappedTasks array
                mappedTasks.push({
                    id: task.id,
                    type: 'task', // or "milestone" or "project" based on your logic
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
            const taskDependencies = dependencies.filter(
                (dependency) => dependency.from === task.id
            );
            taskDependencies.forEach((dependency) => {
                const dependentTask = tasks.find((t) => t.id === dependency.to);
                if (dependentTask) {
                    task.dependencies?.push(dependentTask.id);
                }
            });
        });

        return tasks;
    }
}
