default: slides


ifdef VIRTUAL_ENV
  TOOL_VER:=$(notdir ${VIRTUAL_ENV})
else
  TOOL_VER=_base_
endif

OUTd = __Result/${TOOL_VER}/


slides html :
	sphinx-build -Ea -b $@ -c. IN ${OUTd}$@/

clean:
	rm -rf ${OUTd}

veryclean: clean
	rm -f *-DUMP.xml
	rm -rf __Result/


