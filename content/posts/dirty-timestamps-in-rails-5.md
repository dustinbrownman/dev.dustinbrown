---
title: "Dirty Timestamps in Rails 5"
date: 2019-09-04T22:01:31-07:00
draft: false
tags:
  - ruby
  - rails 5
  - dirty attributes
---

A couple of coworkers and I spent the last couple of days digging into why a test was failing as part of the Rails 5 upgrade. Up to this point, most of the failures we encountered were pretty straight-forward to fix: making sure we treated params as its own object and not a `HashWithIndifferentAccess`, untangling Gem versions, those sort of things.

However, we ran into an issue where a complex, but consistent test was failing, and failing in different ways with each run. 😢

## Debugging the mess

Part of what took us so long was untangling the combination of classes, callbacks, and Resque jobs that made up this part of the code base. Eventually we narrowed it down to one callback.

{{< highlight ruby >}}
class ParentItem
  after_commit :update_children, on: :update

  def update_children
    return unless should_update_children?
    # updating children and more consequences down here
  end

  #...
end
{{< / highlight >}}

Our debugging revealed that before the Rails 5 upgrade (specifically, we were upgrading from Rails 4.2.11.1 to Rails 5.0.7.2), `should_update_children?` always returned `false`. Doing so kept us from dealing with the consequences that happened below that escape clause and allowed the test to pass. But when we upgraded Rails, _sometimes_ `should_update_children?` returned `false`, but more times, it was `true` (__Important note for later__: this callback gets invoked many times during the test set up).

## Where things get dirty

`should_update_children?` is an interesting method with a rich history. Digging through the commit history, its main purpose appeared to be providing a way to _not_ update the children when a certain attribute was updated.

{{< highlight ruby >}}
# Inside some invoker of ParentItem
parent_item = ParentItem.find(id)

# Just adding this timestamp here. Really don't want to update all the children
# and deal with the other consequences.
parent_item.update!(last_pinged_at: Time.zone.now)

class ParentItem
  #...

  def should_update_children?
    # Don't update the children if all we changed was `last_pinged_at`
    !(previous_changes.keys == %w( last_pinged_at updated_at ))
  end
end
{{< / highlight >}}

Before updating the the children, `ParentItem` would check its `previous_changes`. If it was just updating the `last_pinged_at` (and `updated_at`, since we're updating), then it would escape early.

I have mixed feelings about how this was initially implemented, but it worked in Rails 4.2. So what changed?

## Puts-ing care of business

We started stepping through the code, bit by bit, using every bit of `puts`, `p`, and `pry` skills we had to the test. Eventually, we printed some information around where the `ParentItem` was being updated.

{{< highlight ruby >}}
parent_item = ParentItem.find(id)

puts 'ABOUT TO UPDATE THE PARENT ITEM'
puts "name: #{parent_item.name}"
puts "last_pinged_at: #{parent_item.last_pinged_at}"
puts "Time.zone.now: #{Time.zone.now}"
parent_item.update!(last_pinged_at: Time.zone.now)
{{< / highlight >}}

Remember above where I said this `update_children` callback was invoked many times in the test set up. Well it was this invoker up here that was, well, invoking it. So our output looked something like this:

```
ABOUT TO UPDATE THE PARENT ITEM
name: Test Parent
last_pinged_at:
Time.zone.now: 2019-09-05 06:34:09 UTC

ABOUT TO UPDATE THE PARENT ITEM
name: Test Parent
last_pinged_at: 2019-09-05 06:34:09 UTC
Time.zone.now: 2019-09-05 06:34:09 UTC

ABOUT TO UPDATE THE PARENT ITEM
name: Test Parent
last_pinged_at: 2019-09-05 06:34:09 UTC
Time.zone.now: 2019-09-05 06:34:09 UTC
```

## (Not so) dirty timestamps

You'll notice in the first part of the log, `last_pinged_at` is missing, meaning it's `nil`. But you'll notice in the second and third logs, _`last_pinged_at` is the same as the `Time.zone.now` it's about to be set to_. So even though we were updating `last_pinged_at`, it was not considered a `previous_change` because the values were equal*? We needed to do some testing to find out.

In order to test this, we decided to capture `Time.zone.now` into two variables. We'd use each to update the `last_pinged_at` attribute of a `ParentItem` and see if it was marked as a previous change or not.

{{< highlight ruby >}}
# in the rails console
parent_item = ParentItem.first
one = Time.zone.now; two = Time.zone.now

parent_item.update(last_pinged_at: one)

parent_item.previous_changes.keys
=> ['last_pinged_at', 'updated_at']
# this is what we'd expect

parent_item.update(last_pinged_at: two)

parent_item.previous_changes.keys
=> []
# Nope, not a previous change 😱
{{< / highlight >}}

\* note the values aren't actually equal. `one == two` will return `false`, but Rails apparently still sees them as "equivelant" when it comes to if an attribute has changed or not.

As a gut check, we tested this back on Rails 4.2, and got a different result.

{{< highlight ruby >}}
#...
one = Time.zone.now; two = Time.zone.now

parent_item.update(last_pinged_at: one)

parent_item.previous_changes.keys
=> ['last_pinged_at', 'updated_at']
# this is what we'd expect

parent_item.update(last_pinged_at: two)

parent_item.previous_changes.keys
=> ['last_pinged_at', 'updated_at']
# Still marked as dirty
{{< / highlight >}}

So our suspicious was correct. Rails wouldn't mark an attribute as having changed if the value remained the same. Honestly, that's they way it should work. Just unbeknownst to us, we had created a dependency on Rails always capturing previous changes, even if nothing actually changed.

## So now what?

We haven't come on a diffinitive solution for this yet. One prevailing thought is if the invoker doesn't want side-effects for it's update, it should be intentional about skipping them. However, there is something nice about the `ParentItem` guarding against unneeded changes. Either way, relying on the certain attributes becoming dirty for control flow seems like a bad idea.

### One last thing

I did spend time digging through Rails source code (and using the trusty `pry`) to try and understand exactly what changed between rails 4.2 and 5.0. While I definitely found some differences (hello `ActiveModel::AttributeMutationTracker`), I don't understand enough about the underlying implementation to know for sure why these attributes behave differently. If you know, or can point me in the right direction, hit me up on Twitter and I'll add your thoughts with credit here.

__Let's chat. Feel free to respond to my tweet about this post to start a conversation. 🙃__
{{< tweet 1169519933148954625 >}}
