<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:for-each select="/movies/movie">
            <div class="d-flex flex-row" style="min-width: 0; word-wrap: break-word; background-color: #fff; background-clip: border-box; border: 1px solid rgba(0, 0, 0, 0.125); border-radius: 0.25rem; border-bottom-right-radius: 0.25rem; border-bottom-left-radius: 0.25rem; margin-bottom: 1.5rem !important;">
                <div class="p-2">
                    <img><xsl:attribute name="src"><xsl:value-of select="poster"/></xsl:attribute>
                         <xsl:attribute name="alt">"Card image cap"</xsl:attribute>
                         <xsl:attribute name="class">"card-img-top"</xsl:attribute></img>
                </div>
                <div class="p-2">
                    <h2><a><xsl:attribute name="href">movie/<xsl:value-of select="title/name"/>/</xsl:attribute>
                            <xsl:value-of select="title/name"/></a></h2>(<xsl:value-of select="title/year"/>)
                    <p><xsl:for-each select="genres/genre">[<xsl:value-of select="."/>]</xsl:for-each></p>
                    <p><strong><i>Director:</i></strong>
                        <a><xsl:attribute name="href">director/<xsl:value-of select="director//name/first_name"/>
                            _<xsl:value-of select="director//name/last_name"/>/</xsl:attribute>
                            <xsl:value-of select="director//name"/>
                        </a>
                    </p>
                    <p><strong><i>Cast: </i></strong><br/>
                        <xsl:for-each select="cast/main_actors//name">- <a><xsl:attribute name="href">actor/
                            <xsl:value-of select="first_name"/>_<xsl:value-of select="last_name"/>/</xsl:attribute>
                            <xsl:value-of select="."/></a><br/>
                        </xsl:for-each>
                    </p>
                    <p><strong><xsl:value-of select="imbd_info/score"/></strong>/10</p>
                </div>
            </div>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>