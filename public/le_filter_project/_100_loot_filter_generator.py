"""
Last Epoch Loot Filter Generator

A Python library for generating Last Epoch loot filter XML files from JSON definitions.
Provides a clean OOP interface for creating, parsing, and exporting loot filters.
"""

import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import logging


class FilterCondition(ABC):
    """Abstract base class for all filter conditions."""
    
    def __init__(self, condition_data: Dict[str, Any]) -> None:
        """
        Initialize the condition with data from JSON definition.
        
        Args:
            condition_data: Dictionary containing condition parameters
        """
        self.condition_data = condition_data
        self.condition_type = condition_data.get("type", "")
    
    @abstractmethod
    def to_xml(self) -> ET.Element:
        """
        Convert this condition to XML element.
        
        Returns:
            ET.Element: XML representation of the condition
        """
        pass


class AffixCondition(FilterCondition):
    """Condition for matching items based on their affixes."""
    
    def to_xml(self) -> ET.Element:
        """Convert AffixCondition to XML element."""
        condition = ET.Element("Condition")
        condition.set("i:type", "AffixCondition")
        
        # Add affixes
        affixes_elem = ET.SubElement(condition, "affixes")
        for affix_id in self.condition_data.get("affixes", []):
            affix_int = ET.SubElement(affixes_elem, "int")
            affix_int.text = str(affix_id)
        
        # Add comparison parameters
        comparison = ET.SubElement(condition, "comparsion")
        comparison.text = self.condition_data.get("comparison", "MORE")
        
        comparison_value = ET.SubElement(condition, "comparsionValue")
        comparison_value.text = str(self.condition_data.get("comparison_value", 1))
        
        min_on_item = ET.SubElement(condition, "minOnTheSameItem")
        min_on_item.text = str(self.condition_data.get("min_on_same_item", 1))
        
        combined_comparison = ET.SubElement(condition, "combinedComparsion")
        combined_comparison.text = self.condition_data.get("combined_comparison", "MORE")
        
        combined_value = ET.SubElement(condition, "combinedComparsionValue")
        combined_value.text = str(self.condition_data.get("combined_comparison_value", 1))
        
        advanced = ET.SubElement(condition, "advanced")
        advanced.text = str(self.condition_data.get("advanced", False)).lower()
        
        return condition


class ClassCondition(FilterCondition):
    """Condition for matching items usable by specific classes."""
    
    def to_xml(self) -> ET.Element:
        """Convert ClassCondition to XML element."""
        condition = ET.Element("Condition")
        condition.set("i:type", "ClassCondition")
        
        req = ET.SubElement(condition, "req")
        req.text = self.condition_data.get("required_class", "None")
        
        return condition


class RarityCondition(FilterCondition):
    """Condition for matching items based on rarity and legendary properties."""
    
    def to_xml(self) -> ET.Element:
        """Convert RarityCondition to XML element."""
        condition = ET.Element("Condition")
        condition.set("i:type", "RarityCondition")
        
        rarity = ET.SubElement(condition, "rarity")
        rarity.text = self.condition_data.get("rarity", "COMMON")
        
        min_lp = ET.SubElement(condition, "minLegendaryPotential")
        min_lp.text = str(self.condition_data.get("min_legendary_potential", 0))
        
        max_lp = ET.SubElement(condition, "maxLegendaryPotential")
        max_lp.text = str(self.condition_data.get("max_legendary_potential", 4))
        
        min_ww = ET.SubElement(condition, "minWeaversWill")
        min_ww.text = str(self.condition_data.get("min_weavers_will", 0))
        
        max_ww = ET.SubElement(condition, "maxWeaversWill")
        max_ww.text = str(self.condition_data.get("max_weavers_will", 4))
        
        # Add deprecated fields for compatibility
        advanced_dep = ET.SubElement(condition, "advanced_DEPRECATED")
        advanced_dep.text = "false"
        
        req_lp_dep = ET.SubElement(condition, "requiredLegendaryPotential_DEPRECATED")
        req_lp_dep.text = "0"
        
        req_ww_dep = ET.SubElement(condition, "requiredWeaversWill_DEPRECATED")
        req_ww_dep.text = "0"
        
        return condition


class CraftingMaterialsCondition(FilterCondition):
    """Condition for matching crafting materials."""
    
    def to_xml(self) -> ET.Element:
        """Convert CraftingMaterialsCondition to XML element."""
        condition = ET.Element("Condition")
        condition.set("i:type", "CraftingMaterialsCondition")
        
        material_type = ET.SubElement(condition, "NonEquippableItemFilterFlags")
        material_type.text = self.condition_data.get("material_type", "AllCrafting")
        
        return condition


class KeysCondition(FilterCondition):
    """Condition for matching keys and special materials."""
    
    def to_xml(self) -> ET.Element:
        """Convert KeysCondition to XML element."""
        condition = ET.Element("Condition")
        condition.set("i:type", "KeysCondition")
        
        key_type = ET.SubElement(condition, "NonEquippableItemFilterFlags")
        key_type.text = self.condition_data.get("key_type", "AllKeys")
        
        return condition


class LevelCondition(FilterCondition):
    """Condition for matching items based on item level."""
    
    def to_xml(self) -> ET.Element:
        """Convert LevelCondition to XML element."""
        condition = ET.Element("Condition")
        condition.set("i:type", "LevelCondition")
        
        threshold = ET.SubElement(condition, "treshold")  # Note: using original XML spelling
        threshold.text = str(self.condition_data.get("threshold", 0))
        
        level_type = ET.SubElement(condition, "type")
        level_type.text = self.condition_data.get("level_type", "HIGHEST_USABLE_LEVEL")
        
        return condition


class FilterRule:
    """Represents a single filter rule with conditions and visual effects."""
    
    def __init__(self, rule_data: Dict[str, Any]) -> None:
        """
        Initialize a filter rule from JSON data.
        
        Args:
            rule_data: Dictionary containing rule configuration
        """
        self.enabled = rule_data.get("enabled", True)
        self.action = rule_data.get("action", "SHOW")
        self.order = rule_data.get("order", 0)
        self.description = rule_data.get("description", "")
        self.visual_effects = rule_data.get("visual_effects", {})
        self.conditions = self._parse_conditions(rule_data.get("conditions", []))
    
    def _parse_conditions(self, conditions_data: List[Dict[str, Any]]) -> List[FilterCondition]:
        """
        Parse condition data into FilterCondition objects.
        
        Args:
            conditions_data: List of condition dictionaries
            
        Returns:
            List of FilterCondition instances
        """
        conditions = []
        condition_map = {
            "AffixCondition": AffixCondition,
            "ClassCondition": ClassCondition,
            "RarityCondition": RarityCondition,
            "CraftingMaterialsCondition": CraftingMaterialsCondition,
            "KeysCondition": KeysCondition,
            "LevelCondition": LevelCondition,
        }
        
        for condition_data in conditions_data:
            condition_type = condition_data.get("type", "")
            if condition_type in condition_map:
                condition_class = condition_map[condition_type]
                conditions.append(condition_class(condition_data))
            else:
                logging.warning(f"Unknown condition type: {condition_type}")
        
        return conditions
    
    def to_xml(self) -> ET.Element:
        """
        Convert this rule to XML element.
        
        Returns:
            ET.Element: XML representation of the rule
        """
        rule = ET.Element("Rule")
        
        # Basic rule properties
        rule_type = ET.SubElement(rule, "type")
        rule_type.text = self.action
        
        # Add conditions
        conditions_elem = ET.SubElement(rule, "conditions")
        for condition in self.conditions:
            conditions_elem.append(condition.to_xml())
        
        # Visual effects
        color = ET.SubElement(rule, "color")
        color.text = str(self.visual_effects.get("color", 0))
        
        enabled = ET.SubElement(rule, "isEnabled")
        enabled.text = str(self.enabled).lower()
        
        # Deprecated fields for compatibility
        level_dep = ET.SubElement(rule, "levelDependent_deprecated")
        level_dep.text = "false"
        
        min_lvl = ET.SubElement(rule, "minLvl_deprecated")
        min_lvl.text = "0"
        
        max_lvl = ET.SubElement(rule, "maxLvl_deprecated")
        max_lvl.text = "0"
        
        emphasized = ET.SubElement(rule, "emphasized")
        emphasized.text = str(self.visual_effects.get("emphasized", False)).lower()
        
        name_override = ET.SubElement(rule, "nameOverride")
        name_override.text = self.visual_effects.get("name_override", "")
        
        sound_id = ET.SubElement(rule, "SoundId")
        sound_id.text = str(self.visual_effects.get("sound_id", 0))
        
        beam_id = ET.SubElement(rule, "BeamId")
        beam_id.text = str(self.visual_effects.get("beam_id", 0))
        
        order = ET.SubElement(rule, "Order")
        order.text = str(self.order)
        
        return rule


class LootFilterGenerator:
    """Main class for generating Last Epoch loot filter XML files from JSON definitions."""
    
    def __init__(self, definition_file: Optional[Union[str, Path]] = None) -> None:
        """
        Initialize the loot filter generator.
        
        Args:
            definition_file: Path to JSON definition file. If None, will look for
                           'loot_filter_definition.json' in current directory.
        """
        self.definition_file = self._resolve_definition_file(definition_file)
        self.filter_options: Dict[str, Any] = {}
        self.rules: List[FilterRule] = []
        self.logger = self._setup_logger()
    
    def _resolve_definition_file(self, definition_file: Optional[Union[str, Path]]) -> Path:
        """
        Resolve the definition file path.
        
        Args:
            definition_file: User-provided path or None
            
        Returns:
            Path to definition file
        """
        if definition_file is None:
            # Look for default file names
            current_dir = Path.cwd()
            for ext in ["json", "JSON"]:
                default_path = current_dir / f"loot_filter_definition.{ext}"
                if default_path.exists():
                    return default_path
            return current_dir / "loot_filter_definition.json"
        
        return Path(definition_file)
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the generator."""
        logger = logging.getLogger("LootFilterGenerator")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def load_definition(self) -> None:
        """Load and parse the JSON definition file."""
        try:
            if not self.definition_file.exists():
                raise FileNotFoundError(f"Definition file not found: {self.definition_file}")
            
            with open(self.definition_file, "r", encoding="utf-8") as f:
                definition_data = json.load(f)
            
            self.filter_options = definition_data.get("filter_options", {})
            self.rules = [
                FilterRule(rule_data) 
                for rule_data in definition_data.get("rules", [])
            ]
            
            # Sort rules by order (descending - higher order processed first)
            self.rules.sort(key=lambda r: r.order, reverse=True)
            
            self.logger.info(f"Loaded {len(self.rules)} rules from {self.definition_file}")
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in definition file: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading definition file: {e}")
            raise
    
    def generate_xml(self) -> ET.Element:
        """
        Generate the XML structure for the loot filter.
        
        Returns:
            ET.Element: Root XML element of the loot filter
        """
        # Create root element with namespace
        root = ET.Element("ItemFilter")
        root.set("xmlns:i", "http://www.w3.org/2001/XMLSchema-instance")
        
        # Filter metadata
        name = ET.SubElement(root, "name")
        name.text = self.filter_options.get("name", "Generated Filter")
        
        filter_icon = ET.SubElement(root, "filterIcon")
        filter_icon.text = str(self.filter_options.get("filter_icon", 9))
        
        filter_icon_color = ET.SubElement(root, "filterIconColor")
        filter_icon_color.text = str(self.filter_options.get("filter_icon_color", 15))
        
        description = ET.SubElement(root, "description")
        description.text = self.filter_options.get("description", "Generated by LootFilterGenerator")
        
        last_modified = ET.SubElement(root, "lastModifiedInVersion")
        last_modified.text = self.filter_options.get("version", "1.0.0")
        
        loot_filter_version = ET.SubElement(root, "lootFilterVersion")
        loot_filter_version.text = "5"
        
        # Add rules
        rules_elem = ET.SubElement(root, "rules")
        for rule in self.rules:
            if rule.enabled:
                rules_elem.append(rule.to_xml())
        
        return root
    
    def export_filter(self, output_file: Optional[Union[str, Path]] = None) -> Path:
        """
        Export the loot filter to XML file.
        
        Args:
            output_file: Output file path. If None, uses filter name + '.xml'
                        in current directory.
            
        Returns:
            Path to exported file
        """
        if not self.rules:
            self.load_definition()
        
        xml_root = self.generate_xml()
        
        if output_file is None:
            filter_name = self.filter_options.get("name", "Generated Filter")
            # Sanitize filename
            safe_name = "".join(c for c in filter_name if c.isalnum() or c in " -_").strip()
            safe_name = safe_name.replace(" ", "_")
            output_file = Path.cwd() / f"{safe_name}.xml"
        else:
            output_file = Path(output_file)
        
        # Create XML string with proper formatting
        xml_str = ET.tostring(xml_root, encoding="unicode")
        
        # Write to file with proper XML declaration
        with open(output_file, "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(xml_str)
        
        self.logger.info(f"Loot filter exported to: {output_file}")
        return output_file


def main() -> None:
    """Main entry point for command-line usage."""
    import sys
    
    definition_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    try:
        generator = LootFilterGenerator(definition_file)
        output_path = generator.export_filter()
        print(f"Successfully generated loot filter: {output_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
