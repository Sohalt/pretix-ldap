FROM pretix/standalone:stable
USER root
RUN PYTHONPATH=$PYTHONPATH:/pretix/src pip3 install pretix-ldap
USER pretixuser
RUN cd /pretix/src && make production


