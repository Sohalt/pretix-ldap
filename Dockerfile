FROM docker.io/pretix/standalone:stable
USER root
WORKDIR /pretix-ldap/
COPY dist/pretix_ldap*.whl .
RUN PYTHONPATH=$PYTHONPATH:/pretix/src pip3 install pretix_ldap*.whl
USER pretixuser
RUN cd /pretix/src && make production


