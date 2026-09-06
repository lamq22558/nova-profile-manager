"""CLI Entry Point"""

import click
from nova.config import settings
from nova.services.profile_service import ProfileService
from nova.services.browser_service import BrowserService
from nova.services.proxy_service import ProxyService
from tabulate import tabulate

@click.group()
def cli():
    """NOVA Profile Manager CLI"""
    pass

# Profile commands
@cli.group()
def profile():
    """Manage profiles"""
    pass

@profile.command()
@click.option("--name", required=True, help="Profile name")
@click.option("--group", default="Default Group", help="Profile group")
@click.option("--proxy", default="", help="Proxy settings")
@click.option("--url", default="https://facebook.com", help="Target URL")
def create(name, group, proxy, url):
    """Create new profile"""
    service = ProfileService()
    success, prof, error = service.create_profile(
        name=name, group=group, proxy=proxy, url=url
    )
    if success:
        click.secho(f"✓ Profile created: {prof.id}", fg="green")
    else:
        click.secho(f"✗ Error: {error}", fg="red")

@profile.command()
def list():
    """List all profiles"""
    service = ProfileService()
    profiles = service.get_all_profiles()
    
    data = [
        [p.id, p.name, p.group, p.status]
        for p in profiles
    ]
    
    click.echo(tabulate(data, headers=["ID", "Name", "Group", "Status"]))

@profile.command()
@click.argument("profile_id")
def delete(profile_id):
    """Delete profile"""
    service = ProfileService()
    success, error = service.delete_profile(profile_id)
    if success:
        click.secho("✓ Profile deleted", fg="green")
    else:
        click.secho(f"✗ Error: {error}", fg="red")

# Browser commands
@cli.group()
def browser():
    """Control browser instances"""
    pass

@browser.command()
@click.argument("profile_id")
def launch(profile_id):
    """Launch browser for profile"""
    profile_service = ProfileService()
    browser_service = BrowserService()
    
    profile = profile_service.get_profile(profile_id)
    if not profile:
        click.secho(f"✗ Profile not found: {profile_id}", fg="red")
        return
    
    success, error = browser_service.launch_browser(
        profile_id=profile_id,
        profile_data=profile.to_dict(),
        debug_port=profile.debug_port,
    )
    if success:
        click.secho(f"✓ Browser launched: {profile_id}", fg="green")
    else:
        click.secho(f"✗ Error: {error}", fg="red")

@browser.command()
@click.argument("profile_id")
def stop(profile_id):
    """Stop browser instance"""
    service = BrowserService()
    success, error = service.stop_browser(profile_id)
    if success:
        click.secho(f"✓ Browser stopped: {profile_id}", fg="green")
    else:
        click.secho(f"✗ Error: {error}", fg="red")

@browser.command()
def running():
    """List running browsers"""
    service = BrowserService()
    running_profiles = service.get_running_profiles()
    if running_profiles:
        click.echo("Running profiles:")
        for pid in running_profiles:
            click.echo(f"  - {pid}")
    else:
        click.echo("No running browsers")

# Proxy commands
@cli.group()
def proxy():
    """Manage proxies"""
    pass

@proxy.command()
@click.argument("proxy_str")
def add(proxy_str):
    """Add proxy"""
    service = ProxyService()
    success, error = service.add_proxy(proxy_str)
    if success:
        click.secho(f"✓ Proxy added: {proxy_str}", fg="green")
    else:
        click.secho(f"✗ Error: {error}", fg="red")

@proxy.command()
def list():
    """List all proxies"""
    service = ProxyService()
    proxies = service.get_all_proxies()
    for proxy_str in proxies:
        click.echo(f"  - {proxy_str}")

if __name__ == "__main__":
    cli()
