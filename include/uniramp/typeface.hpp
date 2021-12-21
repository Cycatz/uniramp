/*
 * Copyright (c) 2021, Cycatz <cycatz@staque.xyz>
 * BSD-style license; see COPYING
 */

#pragma once

#include <string>

#include <ft2build.h>
#include FT_FREETYPE_H


namespace uniramp
{
class Typeface
{
public:
    Typeface(const std::string &font_path);
    ~Typeface();

    FT_Long num_glyph() { return face->num_glyphs; }
    FT_Int get_pixel_size() { return char_pixel_size; }
    void set_pixel_size(FT_Int pixel_size) { char_pixel_size = pixel_size; }
    double get_coverage(FT_ULong charcode);

private:
    FT_Library library;
    FT_Face face;
    FT_Int char_pixel_size;

    void print_glyph_metrics(FT_Glyph_Metrics *metrics);
    double calculate_coverage(FT_Bitmap *bitmap, int max_size);
};
} /* end namespace uniramp */
