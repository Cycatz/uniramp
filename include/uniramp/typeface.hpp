/*
 * Copyright (c) 2021, Cycatz <cycatz@staque.xyz>
 * BSD-style license; see COPYING
 */

#pragma once

#include <string>

#include <ft2build.h>
#include FT_FREETYPE_H


namespace uniramp {
class Typeface
{
public:
    Typeface(const std::string &font_path);
    ~Typeface();
    FT_Long num_glyph() { return face->num_glyphs; }
    double get_coverage(FT_ULong charcode);

private:
    void print_glyph_metrics(FT_Glyph_Metrics *metrics);
    double calculate_coverage(FT_Bitmap *bitmap, int max_size);
    FT_Library library; 
    FT_Face face;


    FT_Int char_pixel_size; 
};
} /* end namespace uniramp */

