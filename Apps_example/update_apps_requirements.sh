#!/bin/bash

for app_folder in */; do
    pipreqs --force $app_folder
done
