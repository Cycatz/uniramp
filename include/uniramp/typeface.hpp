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
    Typeface(const std::string &font_path, FT_Long face_index);
    ~Typeface();

    FT_Long num_glyph() { return m_face->num_glyphs; }
    FT_Int get_pixel_size() { return m_char_pixel_size; }
    void set_pixel_size(FT_Int pixel_size) { m_char_pixel_size = pixel_size; }

    std::string get_family_name() { return std::string(m_face->family_name); }
    std::string get_style_name() { return std::string(m_face->style_name); }

    double get_coverage(FT_ULong charcode);

private:
    FT_Library m_library;
    FT_Face m_face;
    FT_Int m_char_pixel_size;

    void print_glyph_metrics(FT_Glyph_Metrics *metrics);
    double calculate_coverage(FT_Bitmap *bitmap, int max_size);
};
} /* end namespace uniramp */
