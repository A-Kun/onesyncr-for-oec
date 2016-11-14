import d4.into_DB as DB
import d4.into_XML as XML
import d4.xmltools
import d4.merge
import d4.generating_file.eu as eu
import d4.generating_file.nasa as nasa
import d4.generating_file.oec as oec


if __name__=="__main__":
    oec.get()
    oec.parse()
    print("OEC Done with downloading!")
    print("OEC Write to Database...")
    DB.into_db()
    print('OEC data has been imported to DB')

    eu.get()
    eu.parse()
    print("eu Done with downloading!")

    nasa.get()
    nasa.parse()
    print("NASA Done with downloading!")

    print('merging crash')

    XML.into_xml()
    print('Data has write into XML files and ready to push')
