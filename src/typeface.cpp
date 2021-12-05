/*
 * Copyright (c) 2021, Cycatz <cycatz@staque.xyz>
 * BSD-style license; see COPYING
 */

#include <uniramp/typeface.hpp>

#include <iostream>
#include <cassert>
#include <stdexcept>

namespace uniramp {



Typeface::Typeface(const std::string &font_path) : char_pixel_size(32)
{
    FT_Error error; 

    error = FT_Init_FreeType(&library);  
    if (error) {
        throw std::runtime_error("Error initializing the font library");
    }

    error = FT_New_Face(library, font_path.data(), 0, &face);
    if (error == FT_Err_Unknown_File_Format)  {
        throw std::runtime_error("Unknown font file format");
    } else if (error) {
        throw std::runtime_error("Unknown error");
    }
}

double Typeface::calculate_ratio(FT_Bitmap *bitmap, int max_size)
{

    FT_Int i, sum = 0;
    FT_Int bitmap_size = bitmap->width * bitmap->rows;
    FT_UShort gray_level = bitmap->num_grays;

    /* Iterate the bitmap */ 

    for (i = 0; i < bitmap_size; i++) {
        sum += bitmap->buffer[i];
    }
    return sum / (double) (max_size * gray_level);
}

void Typeface::load_glyph(FT_ULong charcode)
{
    FT_Error error;
    FT_UInt glyph_index;

    /* Set character pixel sizes, default is 1em x 1em = 32 x 32 pixels */
    error = FT_Set_Pixel_Sizes(face, 0, char_pixel_size);
    if (error) {
        throw std::runtime_error("Unknown error");
    }

    glyph_index = FT_Get_Char_Index(face, charcode); 
    error = FT_Load_Glyph(face, glyph_index, FT_LOAD_DEFAULT);

    if (error) {
        throw std::runtime_error("Unknown error");
    }

    error = FT_Render_Glyph( face->glyph,           /* glyph slot  */
                            FT_RENDER_MODE_NORMAL); /* render mode */
    if (error) {
        throw std::runtime_error("Unknown error");
    }

    /* The values are expressed in 26.6 fractional pixel format, which means 1 unit = 1/64 pixel */
    FT_Pos width  = (face->glyph->metrics.horiAdvance) >> 6;
    FT_Pos height = (face->glyph->metrics.vertAdvance) >> 6;

    /* Not all fonts do contain vertical metrics */
    if (height == 0) {
        /* Use global metrics to calculate the height */ 
        height = (face->ascender - face->descender) * char_pixel_size / face->units_per_EM;
    } else {
        assert(height == ((face->ascender - face->descender) * char_pixel_size / face->units_per_EM));
    }

    std::cout << "Ratio: " << calculate_ratio(&face->glyph->bitmap, width * height) << std::endl;
}
Typeface::~Typeface()
{
    FT_Done_Face(face);
    FT_Done_FreeType(library);
}
} /* end namespace uniramp */