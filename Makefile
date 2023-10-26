BOOK_SUM=book-summary
SUMMARY=SUMMARY.md

# Remove link to non-exist default page (#)
post_process: build_summary
	sed -E -i -e "s/\(#\)/()/g" ${SUMMARY}

# Make SUMMARY.md cargo book-summary
build_summary:
	book-summary -y



