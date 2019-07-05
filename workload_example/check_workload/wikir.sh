path1="/lustre/enwiki-20170201-pages-meta-history14.xml-p006197598p006455571.7z"
chsum1=$(eval md5sum $path1)
comsum1="1ef0f2acff1aac07d235287d98523870  /lustre/enwiki-20170201-pages-meta-history14.xml-p006197598p006455571.7z"
if [ "${chsum1::-75}" == "${comsum1::-75}" ]; then
	echo 'The correct checksum is' "${chsum1::-75}"
	echo 'The tested  checksum is' "${comsum1::-75}" 
	echo "The tested  checksum is correct!"	
else 
	echo 'The correct checksum is' "${chsum1::-75}"
        echo 'The tested  checksum is' "${comsum1::-75}"
	echo "The tested  checksum is incorrect!"
fi

path2="/lustre/enwiki-20170201-pages-meta-history14.xml-p007414802p007640995.7z"
chsum2=$(eval md5sum $path2)
comsum2="fa8481bffd34bf078d9d1b2ec7d60419  /lustre/enwiki-20170201-pages-meta-history14.xml-p007414802p007640995.7z"
if [ "${chsum2::-75}" == "${comsum2::-75}" ]; then
	echo 'The correct checksum is' "${chsum2::-75}"
        echo 'The tested  checksum is' "${comsum2::-75}"
        echo "The tested  checksum is correct!"
else
        echo 'The correct checksum is' "${chsum2::-75}"
        echo 'The tested  checksum is' "${comsum2::-75}"
        echo "The tested  checksum is incorrect!"
fi
