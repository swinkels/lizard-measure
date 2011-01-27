Changelog of lizard-krw
===================================================


0.9 (unreleased)
----------------

- Updated migration 0004: on sqlite it generated an error.

- Updated summary screen with extra parameters.

- Added fields to waterbody.

- Added models Area, Province, Municipality.

- Reversed vertical order of krw measures in krw measure graph.

- Added explicit AlphaScore order ("-min_value").

- Refactored portal-tabs. Portal-tabs are now inherited from the
  (overwritten) lizard_ui/lizardbase.html.

- Refactored color fields and AlphaScore.

- Added krw scores page.

- Added legends to krw graphs in adapter/analysis.

- Added lizard_krw fixture.

- Added template parameter to krw_browser.

- Slightly changed layout of krw_browser.

- Changed required field water_type in water_body to optional with
  migration (no backwards migration).


0.8 (2010-12-22)
----------------

- Added migration.

- Added generate_measure_codes management command.


0.7 (2010-12-21)
----------------

- Updated krw score layout.

- Changed measure costs (3x) from float to integer.

- Order Organizations by name.


0.6 (2010-12-20)
----------------

- Renamed krw score classes.

- Fixed saving alpha scores. TODO: refactor goal score/alpha score/color.


0.5 (2010-12-16)
----------------

- Restarted migration steps from 0001.


0.4 (2010-12-16)
----------------

- Manually changed migrations. Not sure yet if it works correctly.


0.3 (2010-12-16)
----------------

- New measure model and accompanying models + migrations.

- Adjusted measure screen.


0.2 (2010-12-16)
----------------

- Krw adapter can now show alternative maps.

- Area_search now matches ident instead of name.

- Fixed reverse urls.

- Added WaterBody.ident.

- Added initial South migration.


0.1 (2010-12-07)
----------------

- Copy the following items from krw-waternet:

   - models
   - views
   - urls
   - templates
   - layers
   - admin
   - js/css

- Initial library skeleton created by nensskel.  [Jack]