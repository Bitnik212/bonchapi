from bonch.msg.BonchMessageModel import BonchMessageModel


class BonchMessageParser:

    def messages(self, soup) -> list[BonchMessageModel] or None:
        """
        парсер
        """
        table = soup.find("table", attrs={"class": "simple-little-table"})
        msgs: list[BonchMessageModel] = []
        if str(table).find("Сообщений не найдено") != -1:
            return None
        for msg in table.tbody.find_all("tr"):
            try:
                int(msg["id"].replace("tr_", ""))
                msgs.append(self.__parse_message(msg))
            except:
                continue
        return msgs

    @staticmethod
    def __parse_message(soup) -> BonchMessageModel:
        """

        :param soup:
        :return:
        """
        tempid = soup["id"].replace("tr_", "")
        temppid = soup.find_all("td")[0]["onclick"].split("(")[1].replace(");", "")
        global id, readed
        id = 0
        if tempid == temppid:
            id = tempid
        trs = soup.find_all("td")
        readed = True
        try:
            if (soup["style"] == "font-weight: bold !important;"):
                readed = False
        except:
            pass
        date = trs[0].text.split(" ")
        time = trs[0].small.text
        date = date[0]
        title = trs[1].text.replace("\n", "").replace("\r", "").replace("  ", "")
        if title[0:1] == " ":
            title = title[1:]
        files = []
        for file in trs[2].find_all("a"):
            files.append({"name": file.text, "href": file["href"]})
        sender = trs[3].text

        return BonchMessageModel(
            id=int(id),
            readed=readed,
            sender=sender,
            date=date,
            time=time,
            title=title,
            files=[BonchMessageModel.Files(
                name=file['name'],
                href=file['href']
            ) for file in files]
        )

        # return {
        #         "id": int(id),
        #         "readed": readed,
        #         "sender": sender,
        #         "date": date,
        #         "time": time,
        #         "title": title,
        #         "files": files
        #     }
