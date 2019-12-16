<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:for-each select="//cast//person">
            <div class="d-flex flex-row" style="min-width: 0; word-wrap: break-word; background-color: #fff; background-clip: border-box;border: 1px solid rgba(0, 0, 0, 0);border-radius: 0.02rem;border-bottom-right-radius: 0.02rem;border-bottom-left-radius: 0.02rem;">
                <div class="p-2">
                    <h5>
                        &#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;
                        <a>
                            <xsl:attribute name="href">
                                actor/
                                <xsl:value-of select="name/first_name"/>
                                _
                                <xsl:value-of select="name/last_name"/>
                                /
                            </xsl:attribute>
                            <xsl:value-of select="name"/>
                        </a>
                    </h5>
                </div>
            </div>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>

