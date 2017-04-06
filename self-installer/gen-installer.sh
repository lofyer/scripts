#!/bin/sh -e
echo '#!/bin/sh -e
sed -e '1,/^exit$/d' "$0" | tar xzf - && ./project/Setup
exit' > installer

tar czf - project >> installer
chmod +x installer
