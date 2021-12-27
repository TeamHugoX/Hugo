# Hugo - UserBot
# Copyright (C) TeamHugoX
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in <https://www.github.com/TeamHugoX/Hugo/blob/main/LICENSE/>.

FROM teamhugox/hugo:main
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && git clone https://github.com/TeamHugoX/Hugo.git /root/TeamHugoX/ \
    && pip3 install --no-cache-dir -r root/TeamHugoX/requirements.txt \
    && pip3 install av --no-binary av
WORKDIR /root/TeamHugoX/
CMD ["bash", "resources/startup/startup.sh"]
