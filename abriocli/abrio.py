import click

import component.component as Component
import project.project as Project




@click.group()
def cli():
    '''
    Abrio Core Command Line Interface

        .________        _______       ______        ________      ______
        /_______/\     /_______/\     /_____/\      /_______/\    /_____/\
        \::: _  \ \    \::: _  \ \    \:::_ \ \     \__.::._\/    \:::_ \ \
        .\::(_)  \ \    \::(_)  \/_    \:(_) ) )_      \::\ \      \:\ \ \ \
        ..\:: __  \ \    \::  _  \ \    \: __ `\ \     _\::\ \__    \:\ \ \ \
        ...\:.\ \  \ \    \::(_)  \ \    \ \ `\ \ \   /__\::\__/\    \:\_\ \ \
        ....\__\/\__\/     \_______\/     \_\/ \_\/   \________\/     \_____\/  '''
    pass

# Croup Command for Project
@cli.group()
def project() :
    '''
    Create and manage a project
    '''
    pass


# Group Command for component
@cli.group()
def component() :
    '''
    Create and manage a component
    '''
    pass

project.add_command(Project.init)
project.add_command(Project.deploy)
project.add_command(Project.stop)
project.add_command(Project.status)

component.add_command(Component.init)
component.add_command(Component.upload)
component.add_command(Component.rm)
component.add_command(Component.ls)
