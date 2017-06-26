# -*- coding: utf8 - *-
from __future__ import (absolute_import, print_function, unicode_literals,
                        with_statement)

from unihan_db.tables import (UnhnLocation, UnhnLocationkXHC1983, UnhnReading,
                              kCantonese, kCheungBauer, kCihaiT, kDaeJaweon,
                              kDefinition, kFenn, kHanYu, kHanyuPinlu,
                              kHanyuPinyin, kHDZRadBreak, kIICore,
                              kIICoreSource, kIRGDaeJaweon, kIRGHanyuDaZidian,
                              kIRGKangXi, kMandarin, kRSAdobe_Japan1_6,
                              kRSJapanese, kRSKangXi, kRSKanWa, kRSKorean,
                              kRSUnicode, kSBGY, kTotalStrokes, kXHC1983)


def import_char(c, char):
    if 'kDefinition' in char:
        for d in char['kDefinition']:
            c.kDefinition.append(kDefinition(definition=d))
    if 'kCantonese' in char:
        for d in char['kCantonese']:
            c.kCantonese.append(kCantonese(definition=d))
    if 'kMandarin' in char:
        d = char['kMandarin']
        c.kMandarin.append(kMandarin(
            hans=d['zh-Hans'],
            hant=d['zh-Hant'],
        ))

    if 'kTotalStrokes' in char:
        d = char['kTotalStrokes']
        c.kTotalStrokes.append(kTotalStrokes(
            hans=d['zh-Hans'],
            hant=d['zh-Hant'],
        ))

    if 'kHanyuPinyin' in char:
        for d in char['kHanyuPinyin']:
            k = kHanyuPinyin()
            for loc in d['locations']:
                k.locations.append(UnhnLocation(
                    volume=loc['volume'],
                    page=loc['page'],
                    character=loc['character'],
                    virtual=loc['virtual'],
                ))
            for reading in d['readings']:
                k.readings.append(UnhnReading(reading=reading))
            c.kHanyuPinyin.append(k)

    if 'kHanYu' in char:
        k = kHanYu()
        for d in char['kHanYu']:
            k.locations.append(UnhnLocation(
                volume=d['volume'],
                page=d['page'],
                character=d['character'],
                virtual=d['virtual'],
            ))
        c.kHanYu.append(k)

    if 'kIRGHanyuDaZidian' in char:
        for d in char['kIRGHanyuDaZidian']:
            k = kIRGHanyuDaZidian()
            k.locations.append(UnhnLocation(
                volume=d['volume'],
                page=d['page'],
                character=d['character'],
                virtual=d['virtual'],
            ))
            c.kIRGHanyuDaZidian.append(k)

    if 'kXHC1983' in char:
        for d in char['kXHC1983']:
            k = kXHC1983()
            for loc in d['locations']:
                k.locations.append(UnhnLocationkXHC1983(
                    page=loc['page'],
                    character=loc['character'],
                    entry=loc['entry'],
                    substituted=loc['substituted'],
                ))
            k.readings.append(UnhnReading(reading=d['reading']))
            c.kXHC1983.append(k)

    if 'kCheungBauer' in char:
        for d in char['kCheungBauer']:
            k = kCheungBauer(
                radical=d['radical'],
                strokes=d['strokes'],
                cangjie=d['cangjie'],
            )

            for reading in d['readings']:
                k.readings.append(UnhnReading(reading=reading))
            c.kCheungBauer.append(k)

    if 'kRSAdobe_Japan1_6' in char:
        for d in char['kRSAdobe_Japan1_6']:
            c.kRSAdobe_Japan1_6.append(kRSAdobe_Japan1_6(
                type=d['type'],
                cid=d['cid'],
                radical=d['radical'],
                strokes=d['strokes'],
                strokes_residue=d['strokes-residue'],
            ))

    if 'kCihaiT' in char:
        for d in char['kCihaiT']:
            c.kCihaiT.append(kCihaiT(
                page=d['page'],
                row=d['row'],
                character=d['character'],
            ))

    if 'kIICore' in char:
        for d in char['kIICore']:
            k = kIICore(priority=d['priority'])
            for s in d['sources']:
                k.sources.append(kIICoreSource(
                    source=s
                ))
            c.kIICore.append(k)

    if 'kDaeJaweon' in char:
        k = kDaeJaweon()
        d = char['kDaeJaweon']
        k.locations.append(UnhnLocation(
            page=d['page'],
            character=d['character'],
            virtual=d['virtual'],
        ))
        c.kDaeJaweon.append(k)

    if 'kIRGKangXi' in char:
        k = kIRGKangXi()
        for d in char['kIRGKangXi']:
            k.locations.append(UnhnLocation(
                page=d['page'],
                character=d['character'],
                virtual=d['virtual'],
            ))
        c.kIRGKangXi.append(k)

    if 'kIRGDaeJaweon' in char:
        k = kIRGDaeJaweon()
        for d in char['kIRGDaeJaweon']:
            k.locations.append(UnhnLocation(
                page=d['page'],
                character=d['character'],
                virtual=d['virtual'],
            ))
        c.kIRGDaeJaweon.append(k)

    if 'kFenn' in char:
        for d in char['kFenn']:
            c.kFenn.append(kFenn(
                phonetic=d['phonetic'],
                frequency=d['frequency']
            ))

    if 'kHanyuPinlu' in char:
        for d in char['kHanyuPinlu']:
            c.kHanyuPinlu.append(kHanyuPinlu(
                phonetic=d['phonetic'],
                frequency=d['frequency']
            ))

    if 'kHDZRadBreak' in char:
        d = char['kHDZRadBreak']
        k = kHDZRadBreak(
            radical=d['radical'],
            ucn=d['ucn']
        )
        k.locations.append(UnhnLocation(
            volume=d['location']['volume'],
            page=d['location']['page'],
            character=d['location']['character'],
            virtual=d['location']['virtual'],
        ))
        c.kHDZRadBreak.append(k)

    if 'kSBGY' in char:
        for d in char['kSBGY']:
            k = kSBGY()
            k.locations.append(UnhnLocation(
                page=d['page'],
                character=d['character'],
            ))
            c.kSBGY.append(k)

    rs_fields = [  # radical-stroke fields, since they're the same structure
        ('kRSUnicode', kRSUnicode, c.kRSUnicode,),
        ('kRSJapanese', kRSJapanese, c.kRSJapanese,),
        ('kRSKangXi', kRSKangXi, c.kRSKangXi,),
        ('kRSKanWa', kRSKanWa, c.kRSKanWa,),
        ('kRSKorean', kRSKorean, c.kRSKorean,),
    ]

    for f, model, column in rs_fields:
        if f in char:
            for d in char[f]:
                k = model(
                    radical=d['radical'],
                    strokes=d['strokes'],
                    simplified=d['simplified']
                )
                column.append(k)
