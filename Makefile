PACKAGE := $(shell basename *.spec .spec)
ARCH = noarch
RPMBUILD = rpmbuild --define "_topdir %(pwd)/rpmbuild" \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %(pwd)/rpms" \
	--define "_srcrpmdir %{_rpmdir}" \
	--define "_sourcedir  %{_topdir}"
PREFIX = ${DESTDIR}/usr

all: rpms

clean:
	rm -rf dist/ build/ rpmbuild/ rpms/
	rm -rf docs/*.gz MANIFEST *~ *.egg-info
	find . -name '*.pyc' -exec rm -f {} \;

build: clean
	python setup.py build -f

install: build
	python setup.py install -f --prefix ${PREFIX}

reinstall: uninstall install

install_rpms:
	yum install rpms/${ARCH}/${PACKAGE}*.rpm

uninstall: clean
	rm -f ${PREFIX}/bin/${PACKAGE}
	rm -rf ${PREFIX}/lib/python2.*/site-packages/${PACKAGE}

uninstall_rpms: clean
	rpm -e ${PACKAGE}

sdist:
	python setup.py sdist

prep_rpmbuild: build sdist
	mkdir -p rpmbuild
	mkdir -p rpms
	cp dist/*.gz rpmbuild/

rpms: prep_rpmbuild
	${RPMBUILD} -ba ${PACKAGE}.spec

srpm: prep_rpmbuild
	${RPMBUILD} -bs ${PACKAGE}.spec
