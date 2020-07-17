FROM pretix/standalone:stable
USER root
WORKDIR /pretix-ldap/
#COPY src/requirements.txt .
#RUN PYTHONPATH=$PYTHONPATH:/pretix/src pip3 install -r requirements.txt
COPY src/ .
RUN PYTHONPATH=$PYTHONPATH:/pretix/src pip3 install .
USER pretixuser
RUN cd /pretix/src && make production


