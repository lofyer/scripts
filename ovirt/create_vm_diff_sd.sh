#!/bin/bash
curl -k -v -u "admin@internal:admin" \
-H "Content-type: application/xml" \
-d '<vm><name>myvm</name><cluster><name>Default</name></cluster><template><name>centos-tmp</name></template><stateless>true</stateless><disks> <clone>True</clone><disk id="6b2aef03-403e-4221-87ee-4065e17365d0"><storage_domains><storage_domain id="0133a3df-991b-4d01-93bb-179a40d8899b"/></storage_domains></disk></disks></vm>' 'https://localhost/api/vms'
