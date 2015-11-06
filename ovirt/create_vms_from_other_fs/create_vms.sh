#!/bin/bash
for i in `seq 13 24`
do
    ./create_vm.sh admin win7-11-$i Host_11 win7-11-student ed8a5266-0952-4b11-853a-6397019216b4 6a09048d-040d-41e0-b9cd-944ad9e740c2 98181734-ee9d-4120-b063-e373146fb836 6a09048d-040d-41e0-b9cd-944ad9e740c2
    ./create_vm.sh admin win7-12-$i Host_12 win7-12-student b4b8aec6-38d7-4738-8243-c9acb5139c5a 4a7b4f38-43b9-427a-b48e-eccf0c44e34b 7c194bae-6bda-4124-be9a-05bb8bfb482f 4a7b4f38-43b9-427a-b48e-eccf0c44e34b
done
