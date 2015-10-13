#!/bin/bash
echo "./create.sh adminpass vm_name cluster_name template_name disk1_uuid target_sd_uuid disk2_uuid target_sd_uuid"
curl -k -v -u "admin@internal:$1" \
-H "Content-type: application/xml" \
-d "<vm><name>$2</name><cluster><name>$3</name></cluster><template><name>$4</name></template><disks><clone>True</clone><disk id='$5'><storage_domains><storage_domain id='$6'/></storage_domains></disk><disk id='$7'><storage_domains><storage_domain id='$8'/></storage_domains></disk></disks></vm>" 'https://localhost/api/vms'
