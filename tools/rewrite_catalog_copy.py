"""One-shot copy migration for 0.4. Physical descriptions, not development commentary."""
from pathlib import Path
import json
from catalog import load_catalog, MOD

DESCRIPTIONS={
'silica':'Crushed silicate grains used to melt laboratory glass and fire porous ceramics.',
'glass':'Chemically resistant glass for culture vessels, instruments and filtration assemblies.',
'mineral-nutrients':'A stable blend of mineral salts that feeds pioneer microorganisms.',
'microbial-culture':'A sealed inoculum of hardy microorganisms for nutrient processing and ecological seeding.',
'algal-biomass':'Cultivated algae rich in organic carbon. Feedstock for compost, membranes and biological fuels.',
'compost':'A living mixture of decomposed biomass and microorganisms that enriches mineral soil.',
'biochar':'Porous carbon that retains nutrients, stabilizes soil and adsorbs impurities.',
'activated-carbon':'High-surface-area carbon for purification cartridges and chemical processing.',
'filter-cartridge':'A replaceable sorbent cartridge for atmospheric scrubbers and water filters.',
'spent-filter':'A saturated cartridge containing recoverable carbon, glass and captured contaminants.',
'soil-substrate':'A stable rooting medium composed of mineral grains, compost and porous carbon.',
'seed-mix':'A blend of pioneer seeds and microbial cultures adapted to recovering ground.',
'ceramic-membrane':'A porous, heat-resistant barrier that separates suspended contaminants from process water.',
'thermal-buffer':'A charged heat-transfer cartridge for climate exchangers and sheltered habitats.',
'depleted-thermal-buffer':'A discharged heat-transfer cartridge. Its casing and working medium can be reconditioned.',
'neutralization-charge':'Reactive minerals and carbon that bind dissolved contaminants into separable sludge.',
'hazardous-sludge':'Concentrated industrial contaminants. Vitrification locks the residue into an inert matrix.',
'vitrified-waste':'An inert glass-mineral aggregate suitable for durable construction materials.',
'biofilm':'A cultivated polymer matrix used in membranes, composite reinforcement and pheromone carriers.',
'ecological-data':'Preserved field samples documenting soil structure, microbial activity and pioneer growth.',
'climate-data':'Instrument samples recording atmospheric composition, heat transfer and water-cycle recovery.',
'biosphere-data':'Complex habitat samples used to study interactions within established ecological communities.',
'thermophile-culture':'Heat-tolerant organisms cultivated in mineral-rich volcanic conditions.',
'heavy-metal-cake':'A concentrated mixture of metals separated from contaminated scrap and processing residues.',
'holmium-catalyst':'A stabilized holmium catalyst that supports resilient biological and electrochemical systems.',
'symbiotic-culture':'A balanced consortium of Gleban organisms used to establish diverse habitats.',
'biodiversity-matrix':'An organized community of thermophiles, symbionts and mineral catalysts for habitat restoration.',
'gaia-cell':'A biological coordination cartridge consumed by planetary beacons to maintain a synchronized ecosystem network.',
'ecology-science-pack':'A research package containing ecological samples, preserved media and analytical electronics.',
'climate-science-pack':'A research package combining climate measurements with specialized planetary cultures.',
'restoration-science-pack':'A research package produced from the operating data of a coordinated living-world network.',
'clean-water':'High-purity water for sensitive biological cultures, thermal circuits and chemical processing.',
'oxygen':'Concentrated oxygen for clean metallurgy, nutrient preparation and oxidation reactions.',
'hydrogen':'A light reducing gas used in metallurgy and synthetic fuel production.',
'electrolyte':'An aqueous mineral electrolyte for selective metal recovery and electrochemical reactions.',
'bioleachate':'A biologically active solution that releases useful metals from mineral feedstocks.',
'toxic-effluent':'Contaminated process liquid containing captured pollutants and dissolved industrial residues.',
'algae-vat':'An agitated, temperature-regulated culture vessel for growing microorganisms and algal biomass.',
'composter':'An aerated processing bed that converts organic feedstock into compost, biofilm and biochar.',
'hydroponics-bay':'A controlled growing enclosure that supplies crops with circulating water, nutrients and sheltered light.',
'electrolyzer':'An electrochemical cell bank for gas separation, buffer charging and low-emission chemical processing.',
'reclamation-plant':'A closed-loop separator that recovers useful materials and process water from spent filters and effluent.',
'materials-kiln':'An electrically heated furnace for firing ceramics, melting glass and vitrifying hazardous residues.',
'pyrolyzer':'A sealed high-temperature retort that converts carbon-rich feedstock into concentrated industrial reagents. Produces substantial emissions and toxic residues.',
'air-scrubber':'A forced-air filtration unit that captures airborne pollutants in replaceable sorbent cartridges.',
'soil-enricher':'A mixing and injection station that distributes mineral substrate, microbial culture and water into recovering soil.',
'seed-disperser':'A metered broadcast system that distributes pioneer seeds and soil treatments across suitable habitat.',
'watershed':'A treatment reservoir that restores water quality and supports a stable local water cycle.',
'thermal-exchanger':'A high-power heat-transfer installation that regulates ecological thermal conditions using rechargeable buffer cartridges.',
'detoxifier':'A chemical binding plant that concentrates environmental contaminants into hazardous sludge for treatment.',
'pheromone-dampener':'A controlled-release diffuser that moderates native aggression with a sustained supply of biological pheromone carriers.',
'forcing-tower':'An industrial reaction stack that rapidly alters atmospheric chemistry while releasing pollution and accumulating toxic residues.',
'basalt-conditioner':'A heavy mineral-conditioning station that weathers volcanic feedstock into biologically useful substrate.',
'fulgoran-reclaimer':'A scrap-remediation installation that separates heavy metals and conditions contaminated mineral residues.',
'spore-tower':'A vertical filtration and culture system that balances airborne spores and cultivates symbiotic organisms.',
'cryogenic-garden':'An insulated, heated growing installation that maintains living cultures and water circulation in extreme cold.',
'sanctuary':'A sheltered habitat complex that combines specialized cultures into a resilient ecological community.',
'planetary-beacon':'A planetary coordination station that synchronizes habitat maintenance and records the operating state of the living-world network.',
'ecology-monitor':'An instrument console that broadcasts ecological fitness, contamination, resistance and pollution readings to the circuit network.',
'alloy-stock':'An iron-reinforced mineral composite used for structural frames, storage casings and firearm stocks.',
'carbine':'A compact automatic carbine chambered for standard ballistic magazines.',
'ballistic-magazine':'Ten copper-jacketed cartridges for automatic weapons and sentry turrets.',
'field-dressing':'A sterile biofilm dressing that accelerates wound closure and restores health.',
'field-armor':'A fitted expedition suit with reinforced impact panels and chemical-resistant outer layers.',
'sentry-turret':'A belt-fed automatic sentry mounted in a reinforced, rotating armored housing.',
'field-barricade':'A riveted, stone-filled barrier that absorbs impacts and resists corrosive attack.',
'induction-rifle':'A battery-fed precision rifle that discharges concentrated electrical energy into its target.',
'induction-cell':'A sealed power cell providing ten electrical discharges for an induction rifle.',
'arc-turret':'A capacitor-fed electrical turret with a high-capacity buffer and a sustained demand for power.',
'composite-wall':'A layered steel and biological-composite barrier with strong impact and acid resistance.',
'expedition-armor':'Powered modular armor with a six-by-six equipment grid and expanded carrying capacity.',
'lance-rifle':'A magnetic accelerator that drives dense projectiles through armored targets along a straight firing line.',
'lance-cell':'A dense-core rail projectile capable of penetrating multiple targets along its firing line.',
'lance-turret':'A reinforced magnetic accelerator for long-range defense against heavily armored targets. Requires charged power reserves and rail ammunition.',
'bastion-armor':'Heavy powered armor with a ten-by-ten equipment grid, reinforced plating and expanded carrying capacity.',
'ecoshield-equipment':'A powered field generator that absorbs incoming damage and recharges from the equipment grid.'
}

def main():
    catalog=load_catalog()
    paths=[MOD/'shared/catalog.lua', MOD/'shared/expedition.lua']
    entries=catalog['items']+catalog['fluids']+catalog['machines']+catalog.get('expedition',[])
    for path in paths:
        text=path.read_text()
        for x in entries:
            if x['name'] in DESCRIPTIONS:
                old=json.dumps(x['description'],ensure_ascii=False)
                new=json.dumps(DESCRIPTIONS[x['name']],ensure_ascii=False)
                text=text.replace(old,new)
        path.write_text(text)
if __name__=='__main__':main()
