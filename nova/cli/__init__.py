"""CLI Commands"""
try:
    import click
    from nova.services import ProfileService
    
    @click.group()
    def cli():
        pass
    
    @cli.group()
    def profile():
        pass
    
    @profile.command()
    @click.option('--name', required=True)
    @click.option('--group', default='Default Group')
    def create(name, group):
        success, prof, error = ProfileService.create_profile(name=name, group=group)
        if success:
            click.echo(f"✓ Profile created: {prof['id']}")
        else:
            click.echo(f"✗ Error: {error}")
    
    @profile.command()
    def list():
        profiles = ProfileService.get_all_profiles()
        for p in profiles:
            click.echo(f"  {p['id']} - {p['name']} ({p['group']})")
    
    if __name__ == '__main__':
        cli()
except ImportError:
    pass
