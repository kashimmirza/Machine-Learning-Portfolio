"""
Field definitions for different document types.
Defines which fields to extract from invoices, utility bills, etc.
"""

from typing import List, Dict, Any
from pydantic import BaseModel


class FieldDefinition(BaseModel):
    """Definition of a field to extract."""
    name: str
    description: str
    data_type: str  # string, number, date, etc.
    required: bool = False
    validation_pattern: str = None


# Invoice field definitions
INVOICE_FIELDS: List[FieldDefinition] = [
    FieldDefinition(
        name="invoice_number",
        description="Unique invoice identifier/number",
        data_type="string",
        required=True
    ),
    FieldDefinition(
        name="invoice_date",
        description="Date the invoice was issued",
        data_type="date",
        required=True
    ),
    FieldDefinition(
        name="due_date",
        description="Payment due date",
        data_type="date",
        required=False
    ),
    FieldDefinition(
        name="supplier_name",
        description="Name of the supplier/vendor",
        data_type="string",
        required=True
    ),
    FieldDefinition(
        name="supplier_address",
        description="Supplier's address",
        data_type="string",
        required=False
    ),
    FieldDefinition(
        name="customer_name",
        description="Name of the customer/client",
        data_type="string",
        required=False
    ),
    FieldDefinition(
        name="subtotal",
        description="Subtotal amount before tax",
        data_type="number",
        required=True
    ),
    FieldDefinition(
        name="tax_amount",
        description="Tax/VAT amount",
        data_type="number",
        required=False
    ),
    FieldDefinition(
        name="tax_rate",
        description="Tax/VAT rate percentage",
        data_type="number",
        required=False
    ),
    FieldDefinition(
        name="total_amount",
        description="Total amount including tax",
        data_type="number",
        required=True
    ),
    FieldDefinition(
        name="currency",
        description="Currency code (USD, EUR, GBP, etc.)",
        data_type="string",
        required=False
    ),
    FieldDefinition(
        name="payment_terms",
        description="Payment terms or conditions",
        data_type="string",
        required=False
    ),
    FieldDefinition(
        name="reference_number",
        description="Reference or PO number",
        data_type="string",
        required=False
    ),
]

# Utility bill field definitions
UTILITY_BILL_FIELDS: List[FieldDefinition] = [
    FieldDefinition(
        name="account_number",
        description="Customer account number",
        data_type="string",
        required=True
    ),
    FieldDefinition(
        name="bill_date",
        description="Date the bill was issued",
        data_type="date",
        required=True
    ),
    FieldDefinition(
        name="due_date",
        description="Payment due date",
        data_type="date",
        required=True
    ),
    FieldDefinition(
        name="provider_name",
        description="Utility provider name",
        data_type="string",
        required=True
    ),
    FieldDefinition(
        name="service_address",
        description="Service location address",
        data_type="string",
        required=False
    ),
    FieldDefinition(
        name="billing_period_start",
        description="Start date of billing period",
        data_type="date",
        required=False
    ),
    FieldDefinition(
        name="billing_period_end",
        description="End date of billing period",
        data_type="date",
        required=False
    ),
    FieldDefinition(
        name="meter_reading_previous",
        description="Previous meter reading",
        data_type="number",
        required=False
    ),
    FieldDefinition(
        name="meter_reading_current",
        description="Current meter reading",
        data_type="number",
        required=False
    ),
    FieldDefinition(
        name="consumption",
        description="Total consumption (kWh, m³, etc.)",
        data_type="number",
        required=True
    ),
    FieldDefinition(
        name="consumption_unit",
        description="Unit of consumption (kWh, m³, gallons, etc.)",
        data_type="string",
        required=False
    ),
    FieldDefinition(
        name="unit_rate",
        description="Rate per unit",
        data_type="number",
        required=False
    ),
    FieldDefinition(
        name="charges",
        description="Total charges before tax",
        data_type="number",
        required=True
    ),
    FieldDefinition(
        name="tax_amount",
        description="Tax amount",
        data_type="number",
        required=False
    ),
    FieldDefinition(
        name="total_amount",
        description="Total amount due",
        data_type="number",
        required=True
    ),
    FieldDefinition(
        name="utility_type",
        description="Type of utility (electricity, gas, water, etc.)",
        data_type="string",
        required=False
    ),
]


def get_field_definitions(document_type: str) -> List[FieldDefinition]:
    """Get field definitions for a document type."""
    field_map = {
        "invoice": INVOICE_FIELDS,
        "utility_bill": UTILITY_BILL_FIELDS,
    }
    return field_map.get(document_type, INVOICE_FIELDS)


def create_extraction_prompt(document_type: str, custom_fields: List[str] = None) -> str:
    """
    Create a structured prompt for GPT-4 Vision to extract fields.
    
    Args:
        document_type: Type of document (invoice, utility_bill)
        custom_fields: Optional list of custom field names to extract
    
    Returns:
        Formatted prompt for AI extraction
    """
    fields = get_field_definitions(document_type)
    
    if custom_fields:
        # Add custom fields
        for field_name in custom_fields:
            fields.append(FieldDefinition(
                name=field_name,
                description=f"Extract {field_name}",
                data_type="string",
                required=False
            ))
    
    field_descriptions = "\n".join([
        f"- {field.name}: {field.description} (type: {field.data_type}, {'required' if field.required else 'optional'})"
        for field in fields
    ])
    
    prompt = f"""You are a document data extraction specialist. Extract the following information from this {document_type} image.

FIELDS TO EXTRACT:
{field_descriptions}

INSTRUCTIONS:
1. Carefully analyze the entire document
2. Extract each field value accurately
3. If a field is not found or unclear, use null
4. For dates, use ISO format (YYYY-MM-DD)
5. For numbers, extract numeric values only (no currency symbols)
6. Be precise and verify extracted data

Return the data as a JSON object with the field names as keys.
Example format:
{{
    "field_name_1": "value",
    "field_name_2": 123.45,
    "field_name_3": "2024-01-15",
    "field_name_4": null
}}

Only return the JSON object, no additional text or explanation."""
    
    return prompt
