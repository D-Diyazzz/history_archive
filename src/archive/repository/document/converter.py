from src.archive.domains.document import Document


def document_to_dict(model: Document):
    model_dict = {
        "file_url": model.get_file_url if model.get_file_url else None,
        "title": model.get_title if model.get_title else None,
        "heading": model.get_heading if model.get_heading else None,
        "author": model.get_author if model.get_author else None,
        "description_content": model.get_description_content if model.get_description_content else None,
        "dating": model.get_dating if model.get_dating else None,
        "legends": model.get_legends if model.get_legends else None,
        "format_doc": model.get_format_doc if model.get_format_doc else None,
        "color_palette": model.get_color_palette if model.get_color_palette else None,
        "resolution": model.get_resolution if model.get_resolution else None,
        "compression": model.get_compression if model.get_compression else None,
        "scanner_model": model.get_scanner_model if model.get_scanner_model else None,
        "created_at": model.get_created_at if model.get_created_at else None
    }

    return {k: v for k, v in model_dict.items() if v is not None}


def dict_to_document(document):
    return Document(
        id=document.id,
        file_url=document.file_url,
        title=document.title,
        heading=document.heading,
        author=document.author,
        description_content=document.description_content,
        dating=document.dating,
        legends=document.legends,
        format_doc=document.format_doc,
        color_palette=document.color_palette,
        resolution=document.resolution,
        compression=document.compression,
        scanner_model=document.scanner_model,
        created_at=document.created_at
    )