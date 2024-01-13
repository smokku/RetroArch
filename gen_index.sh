#!/bin/bash
set -e

cd `dirname $0`
for FILE in *; do
	if [ -d "$FILE" ]; then
		pushd $FILE >/dev/null
		echo -n > .index-extended

		for ZIP in *.zip; do
			DATE=`stat --format=%y "$ZIP" | cut -f1 -d' '`
			CRC32=`rhash --crc32c "$ZIP" | cut -f1 -d' '`
			echo "$DATE $CRC32 $ZIP" >> .index-extended
		done

		popd >/dev/null
	fi
done
