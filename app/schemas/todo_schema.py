from marshmallow import Schema, fields, validate


class TodoSchema(Schema):
    """Schema for serializing / deserializing Todo objects."""

    id = fields.Int(dump_only=True)
    title = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=100, error="Title must be between 1 and 100 characters."),
        ],
    )
    complete = fields.Bool(dump_only=True)


class TodoCreateSchema(Schema):
    """Schema for validating todo creation requests."""

    title = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=100, error="Title must be between 1 and 100 characters."),
        ],
    )
