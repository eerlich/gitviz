git log $1 --pretty=format:'{%n  "commit": "%H",%n  "timestamp": "%at"%n},' | sed "$ s/,$//" | sed ':a;N;$!ba;s/\r\n\([^{]\)/\\n\1/g'| awk 'BEGIN { print("[") } { print($0) } END { print("]") }'
